describe('The dashboard', () => {
	it('successfully loads', () => {
		cy.visit('/');
	});

	it('lets you click through to a chart view', () => {
		cy.visit('/');
		cy.contains('a', 'express_server').click();
		cy.url().should('include', '/chart/express_server');
	});

	it("'s home button takens you home", () => {
		cy.visit('/');
		cy.contains('a', 'express_server').click();
		cy.url().should('include', '/chart/express_server');
		cy.contains('Home').click();
		cy.url().should('include', '/');
	});
});

describe('The list view', () => {
	beforeEach(() => {
		cy.visit('/');
	});

	it('contains both example apps', () => {
		cy.contains('express_server');
		cy.contains('flask-server');
	});

	it('has a score for each app', () => {
		cy.get('#express_server-score').should('not.be.empty');
		cy.get('#flask-server-score').should('not.be.empty');
	});

	it('has a CPU value for each app', () => {
		cy.get('#express_server-cpu').should('not.be.empty');
		cy.get('#flask-server-cpu').should('not.be.empty');
	});

	it('has a RAM value for each app', () => {
		cy.get('#express_server-ram').should('not.be.empty');
		cy.get('#flask-server-ram').should('not.be.empty');
	});

	it('has a disk value for each app', () => {
		cy.get('#express_server-disk').should('not.be.empty');
		cy.get('#flask-server-disk').should('not.be.empty');
	});

	it('has a GPU value for each app', () => {
		cy.get('#express_server-gpu').should('not.be.empty');
		cy.get('#flask-server-gpu').should('not.be.empty');
	});

	it('has a VRAM value for each app', () => {
		cy.get('#express_server-vram').should('not.be.empty');
		cy.get('#flask-server-vram').should('not.be.empty');
	});
});
