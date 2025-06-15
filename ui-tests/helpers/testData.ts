export function generateRandomUser() {
  const id = `${Date.now()}-${Math.floor(Math.random() * 1000000)}`;
  return {
    username: `user${id}`,
    email: `user${id}@example.com`,
    password: 'Test123!@#'
  };
}

export function generateArticle(baseName: string, tag: string) {
  const id = Math.floor(Math.random() * 1000000);
  return {
    title: `Test Title - ${baseName} - ${id}`,
    description: 'Test description',
    body: 'This is the body of the test article.',
    tagList: [tag]
  };
}
