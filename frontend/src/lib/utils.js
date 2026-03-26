export let numberOfRows = 50;
export let numberOfCols = 50;
export let scale = 1;
export let grid = Array(numberOfRows)
	.fill(null)
	.map(() => Array(numberOfCols).fill(0));

export function resetGrid() {
	for (let row = 0; row < numberOfRows; row++) {
		grid[row].fill(0);
	}
}

// Pre-compute all grid positions sorted by Euclidean distance from center outward
const centerRow = Math.floor(numberOfRows / 2);
const centerCol = Math.floor(numberOfCols / 2);
const spiralOrder = [];
for (let row = 0; row < numberOfRows; row++) {
	for (let col = 0; col < numberOfCols; col++) {
		const dr = row - centerRow;
		const dc = col - centerCol;
		spiralOrder.push([row, col, dr * dr + dc * dc]);
	}
}
spiralOrder.sort((a, b) => a[2] - b[2]);

export function isPositionAvailableInGrid(startRow, startCol, rowSpan, colSpan) {
	if (
		startRow < 0 ||
		startCol < 0 ||
		startRow + rowSpan > numberOfRows ||
		startCol + colSpan > numberOfCols
	) {
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

	// Scan positions from center outward; center each word on the candidate position
	for (const [row, col] of spiralOrder) {
		const hRow = row - Math.floor(horizontalSize.rowSpan / 2);
		const hCol = col - Math.floor(horizontalSize.colSpan / 2);
		if (isPositionAvailableInGrid(hRow, hCol, horizontalSize.rowSpan, horizontalSize.colSpan)) {
			return { row: hRow, col: hCol, direction: 'horizontal', ...horizontalSize };
		}
		const vRow = row - Math.floor(verticalSize.rowSpan / 2);
		const vCol = col - Math.floor(verticalSize.colSpan / 2);
		if (isPositionAvailableInGrid(vRow, vCol, verticalSize.rowSpan, verticalSize.colSpan)) {
			return { row: vRow, col: vCol, direction: 'vertical', ...verticalSize };
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
	elem.style.fontSize = fontSize + 'vw';
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
	elem.style.fontSize = fontSize + 'vw';
	elem.textContent = word[0];

	if (word[2]) {
		elem.style.color = word[2];
	} else if (word[1] > 3) {
		elem.style.backgroundColor = '#facc15';
		elem.style.color = '#1c1917';
	}
	if (wordPosition.direction == 'vertical') {
		elem.style.writingMode = 'vertical-rl';
	}
	elem.style.gridArea = `${row + 1} / ${col + 1} / span ${rowSpan} / span ${colSpan}`;
	document.querySelector('.container').appendChild(elem);
}
