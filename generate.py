from transformers import AutoModelForCausalLM
from anticipation.sample import generate
from anticipation.convert import events_to_midi, midi_to_events

model = AutoModelForCausalLM.from_pretrained("./nes-model")
#my_events = midi_to_events("generated.mid")
length = 10 # time in seconds
events = generate(model, start_time=0, end_time=length, top_p=.98)#, inputs=my_events)
mid = events_to_midi(events)
mid.save('generated.mid')
