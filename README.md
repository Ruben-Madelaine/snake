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
    - [x] Allow AI
        - [x] Random
        - [x] Myopic vision (Adjacent cells)
        - [ ] Linear vision 
        - [ ] T shape vision
        - [ ] Cone shape vision
        - [ ] 360 linear vision
        - [ ] Loose points based on cause of death
        - [ ] Learn from human games 
    - [ ] Allow game replay

1. AI 
    - [x] Implement a Neural Network
        - [x] Input the cells
        - [x] Output the directions
    - [x] Allow training 
    - [x] Implement a NN manually
    - [x] Save Neural Network configuration and load it 
    - [x] Show statistics
    - [ ] Train to win in short periods
    - [ ] Use a librairy (Pytorch or Tensorflow)
        - [ ] Use Pytorch
 
1. Population
    - [x] Load population
    - [x] Run games
    - [x] Get best game
    - [x] Clone best snake (or the N bests)
    - [x] Mutate clones randomly
    - [x] Save best configuration 

1. Display
    - [x] Basic console output
    - [ ] Animate Wind
    - [ ] Graphical interface
