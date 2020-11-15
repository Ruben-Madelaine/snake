# :snake: Snake

Implementing the well known Snake game with a bit of `A.I.` :robot: flavor !

## :tada: Examples

To be added

## :spiral_calendar: Dates

### :rocket: Started 
Project pitched and started the _11th november 2020_

### :dart: Release date 
First expected release the friday **15th november 2020** 


## Dependencies
1. Set your Virtual Environment:

    ``` bash
    # Download venv librairy
    apt-get install python3-venv -y
    # Create your venv
    py -m venv my_venv
    # Activate your venv
    . venv/bin/activate
    ```
    
    _For more information, go to [Python Virtual Environment Official Documentation](https://docs.python.org/3/library/venv.html)._

1. Install the project dependencies:

    ``` bash
    apt install python3-pip
    pip install numpy
    pip install PTable
    ```

## :clipboard: Tasks

1. Grid
    - [x] Pop up Fruits

1. Snake interface 
    - [x] Move  
    - [x] Eat 
    - [x] Grow 
 
1. Rules 
    - [x] Snake dies when touching it's tail
    - [ ] Biting his tail cuts him in two
    - [ ] Can plant a fruit for later by loosing it's tail 

1. Player
    - [ ] Allow Human to play
    - [ ] Allow AI
        - [x] Random
        - [ ] Linear vision 
        - [ ] T shape vision
        - [ ] Cone shape vision
        - [ ] 360 vision
    - [ ] Allow game replay

1. AI 
    - [ ] Implement a Neural Network
        - [ ] Input the cells
        - [ ] Output the directions
    - [ ] Allow training 
    - [ ] Implement a NN manually
    - [ ] Use a librairy (Pytorch or Tensorflow)
    - [ ] Save Neural Network configuration and load it 
    - [ ] Show statistics
    - [ ] Train to win in short periods
    - [ ] Use Pytorch
 
1. Population
    - [x] Load population
    - [x] Run games
    - [x] Get best game
    - [ ] Clone best snake (or the N bests)
    - [ ] Mutate clones randomly
    - [ ] Save best configuration 

1. Display
    - [x] Basic console output
    - [ ] Animate Wind
    - [ ] Graphical interface
