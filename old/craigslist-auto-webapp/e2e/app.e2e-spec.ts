import { CraigslistAutoWebappPage } from './app.po';

describe('craigslist-auto-webapp App', () => {
  let page: CraigslistAutoWebappPage;

  beforeEach(() => {
    page = new CraigslistAutoWebappPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to app!');
  });
});
