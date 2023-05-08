# Lab 4 - Quiz app

## Story

Imagine, you're a developer at Sunny Entertainment GK, Tokyo. Ni hao. The company is struggling to find customers in Tokyo, so the marketing department proposes to launch a proof-of-concept app for running quizzes. The marketing campaign starts soon and you have to develop the app itself.

The good part is that there is a Quiz API that can be consumed by your application to fetch data about the quizzes.

## Task

1. Pick a frontend framework;
2. Create a web app that has the following functions:
  - it shows a landing page with different quizzes;
  - the user can pick a quiz and play it;
  - after the game has ended, the user can see their score.

3. The app should have attractive UI;
4. Consume [Quiz API](https://late-glitter-4431.fly.dev) to fetch data from backend server.

## Special conditions

You have no restrictions on using third-party packages.

## Grading

Points:

  - view a list of quizzes -- `+1` point
  - view a single quiz -- `+1` point
  - create a user (and storing its ID somewhere) -- `+2` point
  - as a logged user, play a predefined quiz -- `+5` point
    - submit the responses out of the list (multiple choice)
    - show the total score

  - use of your own components - `+1` point.

You can get `+1` point if the app includes a background music player/ sound effects / visual effects (with the condition that on URL change the music continues to play). You can get `+1` point if the app implements some other feature.

## Hints

- If you know a frontend framework - use it!
- If you don't know, use Vue or Nuxt.js.
- Use a CSS library for UI part. You can give a try to Bulma, UIKit, Milligram or Tachyons.
- Use a high-level library to make HTTP requests e.g. axios.
- To track & keep progress in the app, you can use state managers provided by the framework e.g. Redux or Vuex/Pinta.
- Use Postman to test the Quiz API **before** implementing the app itself -- create quizzes, create users, submit responses and so on.
- Keep it simple, commit often, improve gradually.

