<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<h3 align="center">Anticipatory Music Transformer Finetune Skeleton</h3>

### Built With

* Python 3.11
* [Anticipation](https://github.com/jthickstun/anticipation)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites
* pyenv
  ```sh
  pyenv install 3.11
  ```
    ```sh
  pyenv shell 3.11
  ```
Verify that your python version has been switched to 3.11
  ```sh
  python3 --version
  ```

* anticipation
 ```sh
  git clone https://github.com/jthickstun/anticipation.git
  ```
   ```sh
  cd ./anticipation
  ```
   ```sh
  python3 -m pip install .
  ```
   ```sh
  python3 -m pip install -r requirements.txt
  ```
  
<!-- USAGE EXAMPLES -->
## Usage

1. run ``preprocess.py``
2. run ``tokenization.py``
3. Separate ``tokenized-events-*.txt`` into an 80/20 for training/validation. The training/validation text files should be separated into their own directories.
4. Then:
 ```sh
 cat $DATAPATH/training/tokenized-events-*.txt > $DATAPATH/train-ordered.txt
  ```
   ```sh
  cat $DATAPATH/validation/tokenized-events-*.txt > $DATAPATH/valid-ordered.txt
  ```
5. Then:
 ```sh
shuf $DATAPATH/train-ordered.txt > $DATAPATH/train.txt
  ```
6. run ``finetune.py``
7. run ``generate.py``
<p align="right">(<a href="#readme-top">back to top</a>)</p>


