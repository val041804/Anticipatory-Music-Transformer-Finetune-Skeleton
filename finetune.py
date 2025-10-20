from transformers import AutoModelForCausalLM
from transformers import Trainer, TrainingArguments
from datasets import Dataset
import torch

def load_dataset(path):
    with open(path) as f:
        lines = f.readlines()
    return Dataset.from_dict({"text": lines})

def tokenize_fn(batch):
    max_len = 256  # or 256 if needed
    input_ids = [[int(tok) for tok in line.strip().split()[:max_len]] for line in batch["text"]]
    return {
        "input_ids": input_ids,
        "attention_mask": [[1] * len(ids) for ids in input_ids],
        "labels": input_ids
    }

def finetune_model(train_file, valid_file, _output_dir):
    torch.cuda.empty_cache()

    train_ds = load_dataset(train_file)
    valid_ds = load_dataset(valid_file)
    train_ds = train_ds.map(tokenize_fn, batched=True)
    valid_ds = valid_ds.map(tokenize_fn, batched=True)

    model = AutoModelForCausalLM.from_pretrained('stanford-crfm/music-medium-800k').cuda()

    training_args = TrainingArguments(
        output_dir=_output_dir,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        #gradient_accumulation_steps=4,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir="./logs",
        num_train_epochs=5,
        learning_rate=5e-5,
        weight_decay=0.01,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=valid_ds,
    )

    trainer.train()
    trainer.save_model(_output_dir)

def main():
    train_file = input("Training File Path: ")
    valid_file = input("Validation File Path: ")
    name = input("Directory to export model: ")

    finetune_model(train_file, valid_file, name)

if __name__ == "__main__":
    main()
