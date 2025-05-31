import axios from 'axios';
import { generateRandomUser } from './testData';

export async function createRandomUserViaAPI() {
  const user = generateRandomUser();

  const response = await axios.post('http://localhost:3000/api/users', {
    user: {
      username: user.username,
      email: user.email,
      password: user.password,
    }
  });

  return {
    username: response.data.user.username,
    email: response.data.user.email,
    password: user.password,
    token: response.data.user.token,
  };
}


export async function createArticleViaAPI(token: string, article: any) {
  const response = await axios.post(
    'http://localhost:3000/api/articles',
    { article },
    { headers: { Authorization: `Token ${token}` } }
  );

  return {
    ...article,
    slug: response.data.article.slug,
  };
}

export async function addCommentViaAPI(token: string, slug: string, commentData: { body: string }) {
  const response = await fetch(`http://localhost:3000/api/articles/${slug}/comments`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`,
    },
    body: JSON.stringify({ comment: commentData }),
  });

  if (!response.ok) {
    throw new Error(`Failed to add comment: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}
