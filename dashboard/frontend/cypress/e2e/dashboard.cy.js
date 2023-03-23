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
