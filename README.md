# AI Portfolio Projects

This portfolio contains three major AI/ML projects demonstrating skills in algorithm design, reinforcement learning, and neural networks.

## Projects

### 1. Othello AI Player (`othello_ai.py`)

An intelligent Othello (Reversi) game AI using advanced game tree search algorithms.

**Features:**
- **Alpha-Beta Pruning**: Full-depth terminal search for endgame positions
- **Adaptive Strategy**: Automatically switches between terminal alpha-beta (when ≤11 empty squares) and depth-limited midgame search
- **Heuristic Evaluation**: Corner control, edge play, and mobility optimization
- **Move Ordering**: Prioritizes corners, edges, and avoids X-squares (squares adjacent to opponent corners)
- **Tournament Mode**: Can run multiple games for performance evaluation

**Algorithms:**
- `alphaBetaTop`: Terminal alpha-beta search for endgame
- `alphaBetaR`: Recursive alpha-beta with pruning
- `midgameAlphaBeta`: Depth-limited search for midgame positions
- `quickMove`: Fast heuristic-based move selection

**Technical Highlights:**
- Efficient board representation and move generation
- Board symmetry detection for opening book support
- Opponent move minimization strategy
- Complete game logic implementation

---

### 3. Crossword Puzzle Generation

A two-part project for generating American-style crossword puzzles.

#### Part 1: Block Placement (`crossword_block_placement.py`)
- Places blocking squares (#) in a crossword grid to meet target block count
- Ensures symmetry (180-degree rotation)
- Maintains connectivity (all open cells must be reachable)
- Enforces minimum word length (3+ characters)
- Handles seed words and special patterns

**Key Features:**
- Recursive backtracking for block placement
- Graph connectivity validation
- Symmetry enforcement
- Minimum word length constraints

#### Part 2: Word Filling (`crossword_word_filling.py`)
- Fills words into a crossword structure from a dictionary
- Uses constraint satisfaction with backtracking
- Implements multiple strategies:
  - Full backtracking for small puzzles
  - Depth-limited search for medium puzzles
  - Incremental/greedy approaches for large puzzles
- Letter frequency optimization
- Time management for performance

**Key Features:**
- Constraint propagation
- Most-constrained variable selection
- Letter frequency heuristics
- Adaptive strategy selection based on puzzle size

---

### 4. Reinforcement Learning (`reinforcement_learning.py`)

Implementation of value iteration and policy iteration algorithms for finding optimal policies in graph-based environments.

**Features:**
- Graph parsing and representation
- Value iteration for state valuation
- Policy iteration for optimal policy discovery
- Support for custom reward structures
- Visual policy representation
- Discount factor (gamma) for future rewards

**Algorithms:**
- `grfValuePolicy`: Computes state values given a policy
- `grfPolicyFromValuation`: Derives policy from state values
- `grfFindOptimalPolicy`: Iteratively improves policy until convergence

**Use Cases:**
- Grid-world navigation
- Reward-based pathfinding
- Optimal decision making in graph environments

---

### 5. Neural Network - MNIST Digit Classification (`neural_network_mnist.py`)

A complete neural network implementation from scratch (no ML frameworks) for classifying handwritten digits from the MNIST dataset.

**Architecture:**
- Input layer: 784 neurons (28x28 pixel images)
- Hidden layer: 128 neurons with sigmoid activation
- Output layer: 10 neurons (digits 0-9) with softmax activation

**Features:**
- Forward propagation
- Backpropagation algorithm
- Real-time training accuracy visualization
- Batch processing
- One-hot encoding for labels

**Training:**
- 5 epochs
- Learning rate: 0.01
- Stochastic gradient descent
- Real-time accuracy plotting

**Requirements:**
- NumPy for numerical operations
- Matplotlib for visualization
- MNIST dataset files (train-images.idx3-ubyte, train-labels.idx1-ubyte, t10k-images.idx3-ubyte, t10k-labels.idx1-ubyte)

---

## Technical Skills Demonstrated

- **Game AI**: Alpha-beta pruning, minimax algorithm, move ordering, adaptive search strategies
- **Algorithm Design**: Recursive backtracking, constraint satisfaction, graph algorithms
- **Reinforcement Learning**: Value iteration, policy iteration, optimal policy discovery
- **Deep Learning**: Neural network implementation from scratch, backpropagation, activation functions
- **Optimization**: Heuristic search, time management, adaptive strategies, pruning techniques
- **Data Structures**: Graph representation, set operations, efficient data handling, board representations

---

## Author

Aadi Malhotra, pd 1, 2026

