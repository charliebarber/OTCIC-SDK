describe('The chart view', () => {
	beforeEach(() => {
		cy.visit('/chart/express_server');
	});

	it('has a title', () => {
		cy.contains('h2', 'express_server');
	});

	it('displays the language', () => {
		cy.contains('Language: JavaScript');
	});

	it('displays the forecast carbon intensity', () => {
		cy.contains(/Forecast Carbon Intensity: [\d]* gCO2\/kWh/);
	});

	it('displays the actual carbon intensity', () => {
		cy.contains(/Actual Carbon Intensity: [\d]* gCO2\/kWh/);
	});

	it('displays the CPU model', () => {
		cy.contains(/CPU model: .*/);
	});

	it('displays the CPU TDP', () => {
		cy.contains(/CPU TDP: [\d]* W/);
	});

	it('displays the CPU Load Avg', () => {
		cy.contains(/CPU Load Avg: [\d]*/);
	});
});

describe('The SCI pop up', () => {
	beforeEach(() => {
		cy.visit('/chart/express_server');
	});

	it('opens', () => {
		// click the SCI button
		cy.get('.scoreSpan').children('button').click();

		cy.contains('SCI Score Breakdown');
	});
});
