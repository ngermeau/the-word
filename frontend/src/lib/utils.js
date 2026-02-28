export let numberOfRows = 50;
export let numberOfCols = 50;
export let scale = 1;
export let grid = Array(numberOfRows)
	.fill(null)
	.map(() => Array(numberOfCols).fill(0));

export function isPositionAvailableInGrid(startRow, startCol, rowSpan, colSpan) {
	if (startRow + rowSpan > numberOfRows || startCol + colSpan > numberOfCols) {
		return false;
	}

	for (let row = startRow; row < startRow + rowSpan; row++) {
		for (let col = startCol; col < startCol + colSpan; col++) {
			if (grid[row][col] != 0) return false;
		}
	}

	return true;
}

export function findAvailablePosition(word) {
	let horizontalSize = measureWord(word, 'horizontal');
	let verticalSize = measureWord(word, 'vertical');

	// Trying to find fiest valid position horizontal or vertical
	for (let row = 0; row < numberOfRows; row++) {
		for (let col = 0; col < numberOfCols; col++) {
			if (isPositionAvailableInGrid(row, col, horizontalSize.rowSpan, horizontalSize.colSpan)) {
				return { row, col, direction: 'horizontal', ...horizontalSize };
			} else if (isPositionAvailableInGrid(row, col, verticalSize.rowSpan, verticalSize.colSpan)) {
				return { row, col, direction: 'vertical', ...verticalSize };
			}
		}
	}
}

export function measureWord(word, orientation) {
	const cellWidth = window.innerWidth / numberOfCols;
	const cellHeight = window.innerHeight / numberOfRows;
	const fontSize = word[1] / scale;
	const elem = document.createElement('span');
	elem.style.position = 'absolute';
	elem.style.visibility = 'hidden';
	elem.style.textTransform = 'uppercase';
	elem.style.fontSize = fontSize + 'rem';
	if (orientation == 'vertical') {
		elem.style.writingMode = 'vertical-rl';
	}
	elem.style.padding = '1px 2px';
	elem.textContent = word[0];
	document.body.appendChild(elem);
	const rowSpan = Math.ceil(elem.offsetHeight / cellHeight);
	const colSpan = Math.ceil(elem.offsetWidth / cellWidth);
	document.body.removeChild(elem);
	return { rowSpan, colSpan, fontSize };
}

export function drawWord(word, wordPosition) {
	let { row, col, colSpan, rowSpan, fontSize } = wordPosition;

	// Fill in the grid with the word
	grid.slice(row, row + rowSpan).forEach((row) => {
		row.fill(1, col, col + colSpan);
	});

	const elem = document.createElement('div');
	elem.style.fontSize = fontSize + 'rem';
	elem.textContent = word[0];

	// if occurence is high
	if (word[1] > 5) {
		elem.style.backgroundColor = 'black';
		elem.style.color = 'white';
	}
	if (wordPosition.direction == 'vertical') {
		elem.style.writingMode = 'vertical-rl';
	}
	elem.style.gridArea = `${row + 1} / ${col + 1} / span ${rowSpan} / span ${colSpan}`;
	document.querySelector('.container').appendChild(elem);
}
