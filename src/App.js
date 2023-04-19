import React, { useState } from "react";

function Square({
  value,
  clickHandler,
  moveHandler,
  secondMoveHandler,
  counter,
  chose,
}) {
  return (
    // Select spaces until max pieces. If max pieces, make user choose first piece, then destination gridspace
    <button
      className="square"
      onClick={
        counter !== 3 ? clickHandler : chose ? secondMoveHandler : moveHandler
      }
    >
      {value}
    </button>
  );
}

function Board() {
  const [squares, setSquares] = useState(Array(9).fill(null)); // Array of squares
  const [xIsNext, setXIsNext] = useState(true); // Boolean to track turn
  const [counter, setCounter] = useState(0); // counter to track when 6 pieces on board
  const [chose, setChose] = useState(false); // A boolean that tracks whether or not user has chosen first piece or not (moving seq)
  const winner = calculateWinner(squares); // Value that holds value of winner
  let status; // Value that holds the status prompt on the board
  let instructions; // Variable that holds set of instructions

  // Constant checker to see if a winner exists in every rerendered board
  if (winner) {
    status = "Winner: " + winner;
    instructions = "Congratulations " + winner + "!";
  } else {
    if (xIsNext && counter === 3) {
      status = "Currently X's turn";
      instructions = "Click an existing piece to move";
    } else if (xIsNext) {
      status = "Currently X's turn";
      instructions = "Click an open space on the board!";
    } else if (!xIsNext && counter === 3) {
      status = "Currently O's turn";
      instructions = "Click an existing piece to move";
    } else {
      status = "Currently O's turn";
      instructions = "Click an open space on the board!";
    }
  }

  // Change instructions prompt for when use has chosen first piece
  if (chose) {
    instructions = "Choose an open spot!";
  }

  // Handler of clicking square (< 6 pieces on board)
  function clickSquare(i) {
    const newSquares = squares.slice(); // Shallow copy
    // Prevents clicking on same square or after winner determined or if max pieces on board
    if (squares[i] || winner || counter === 3) {
      return;
    }

    // Sets array value to corresponding letter based on turn
    if (xIsNext) {
      newSquares[i] = "X";
    } else {
      newSquares[i] = "O";
      setCounter((currentCount) => {
        // Increments counter (tracking until 3)
        return currentCount + 1;
      });
    }
    setXIsNext(!xIsNext);
    setSquares(newSquares);
  }

  // Function checks if movement from initial to dest is valid given the current move
  // Based on chorus lapilli rules
  function canMove(initialIndex, destinationIndex) {
    const columns = 3;

    const isAdjacent = (initial, destination) => {
      const rowDiff = Math.abs(
        Math.floor(initial / columns) - Math.floor(destination / columns)
      );
      const colDiff = Math.abs((initial % columns) - (destination % columns));
      return rowDiff <= 1 && colDiff <= 1;
    };

    if (!isAdjacent(initialIndex, destinationIndex)) {
      return false;
    }

    // Middle piece checking and emulation:
    // Emulates if winning is possible with shallow copy
    const newSquares = squares.slice();
    if (xIsNext) {
      if (squares[4] === "X") {
        newSquares[initialIndex] = null;
        newSquares[destinationIndex] = "X";
        if (!calculateWinner(newSquares)) {
          return false;
        }
      }
    } else {
      if (squares[4] === "O") {
        newSquares[initialIndex] = null;
        newSquares[destinationIndex] = "O";
        if (!calculateWinner(newSquares)) {
          return false;
        }
      }
    }
    return true;
  }

  // First moving function that makes user move pieces
  // Gen Desc: If you click a valid square, change that square to a 1 to let user know they've clicked it
  function moveHandler(i) {
    if (winner) return; // If a winner has been decided, do not run this function when things are clicked

    let newSquares = squares.slice();

    if (xIsNext) {
      if (squares[i] !== "X") {
        return;
      }
      newSquares[i] = 1;
      setSquares(newSquares);
      setChose(true);
    } else {
      if (squares[i] !== "O") {
        return;
      }
      newSquares[i] = 1;
      setSquares(newSquares);
      setChose(true);
    }
  }

  // Second moving function that makes user move pieces
  // Gen desc: If a user can move their first piece to their second selected grid space, move selected to destination
  function secondMoveHandler(i) {
    if (winner) return; // If a winner has been decided, do not run this function when things are clicked

    if (squares[i] !== null) {
      return;
    }

    // Looping to find where the initial click position is
    let firstidx;
    for (let j = 0; j < 9; ++j) {
      if (squares[j] === 1) {
        firstidx = j;
        break;
      }
    }

    // If moving is viable, then perform all the ops necessary to display that to user
    // If moving not viable, start choice sequence all over again for same person
    if (canMove(firstidx, i)) {
      const newSquares = squares.slice();
      newSquares[firstidx] = null;
      xIsNext ? (newSquares[i] = "X") : (newSquares[i] = "O");
      setSquares(newSquares);
      setXIsNext(!xIsNext);
      setChose(false);
    } else {
      const newSquares = squares.slice()
      xIsNext ? (newSquares[firstidx] = "X") : (newSquares[firstidx] = "O")
      setSquares(newSquares)
      setChose(false)
    }
    return;
  }

  return (
    <div>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square
          value={squares[0]} // Value that displays in the button when pressed "O" or "X"
          clickHandler={() => clickSquare(0)} // Process that displays the value when button is pressed
          moveHandler={() => moveHandler(0)} // Process that allows user to choose a piece to move
          secondMoveHandler={() => secondMoveHandler(0)} // Process that allows user to choose a square to move to
          counter={counter} // Keeps track of how many pieces are on the board
          chose={chose} // Keeps track of whether or not user chose first piece
        />
        <Square
          value={squares[1]}
          clickHandler={() => clickSquare(1)}
          moveHandler={() => moveHandler(1)}
          secondMoveHandler={() => secondMoveHandler(1)}
          counter={counter}
          chose={chose}
        />
        <Square
          value={squares[2]}
          clickHandler={() => clickSquare(2)}
          moveHandler={() => moveHandler(2)}
          secondMoveHandler={() => secondMoveHandler(2)}
          counter={counter}
          chose={chose}
        />
      </div>
      <div className="board-row">
        <Square
          value={squares[3]}
          clickHandler={() => clickSquare(3)}
          moveHandler={() => moveHandler(3)}
          secondMoveHandler={() => secondMoveHandler(3)}
          counter={counter}
          chose={chose}
        />
        <Square
          value={squares[4]}
          clickHandler={() => clickSquare(4)}
          moveHandler={() => moveHandler(4)}
          secondMoveHandler={() => secondMoveHandler(4)}
          counter={counter}
          chose={chose}
        />
        <Square
          value={squares[5]}
          clickHandler={() => clickSquare(5)}
          moveHandler={() => moveHandler(5)}
          secondMoveHandler={() => secondMoveHandler(5)}
          counter={counter}
          chose={chose}
        />
      </div>
      <div className="board-row">
        <Square
          value={squares[6]}
          clickHandler={() => clickSquare(6)}
          moveHandler={() => moveHandler(6)}
          secondMoveHandler={() => secondMoveHandler(6)}
          counter={counter}
          chose={chose}
        />
        <Square
          value={squares[7]}
          clickHandler={() => clickSquare(7)}
          moveHandler={() => moveHandler(7)}
          secondMoveHandler={() => secondMoveHandler(7)}
          counter={counter}
          chose={chose}
        />
        <Square
          value={squares[8]}
          clickHandler={() => clickSquare(8)}
          moveHandler={() => moveHandler(8)}
          secondMoveHandler={() => secondMoveHandler(8)}
          counter={counter}
          chose={chose}
        />
      </div>
      <div className="instructions">{instructions}</div>
    </div>
  );
}

export default function Game() {
  return <Board />;
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
