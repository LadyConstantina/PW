# Lab 2 - HTTP, caching and content negotiation

## Story

Imagine, you're a developer at TwoLines GmbH, a startup from Zurich, Switzerland. The idea of the startup is pretty simple - you develop best-in-class browser experience, with privacy and security in mind. One day, you receive a message from the CTO, Mike.

```
Hey there!

Tomorrow we'll have a presentation for a really biiiig investor.
They say they don't need PPTs. They want at least some proof-of-concept for secure browsers for their toasters.
Can you share with me the executable we used last time for demo?

Cheers,
Mike
```

Yeah, the catch is toasters don't have any browser exeprience!
Nonetheless, you can't remember where you've saved the executable, so you start writing it from scratch.

## Task

1. You have to write a command line program, using [go2web](go2web) executable as a starting point;
2. The program should implement at least the following CLI:
  ```
  go2web -u <URL>         # make an HTTP request to the specified URL and print the response
  go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results
  go2web -h               # show this help
  ```
3. The responses from request should be human-readable (e.g. no HTML tags in the output)

## Special conditions

Any programming language can be used, but not the built-in/third-party libraries for making HTTP requests. GUI applications aren't allowed. The app has to be launched with `go2web` executable.

## Grading

Points:

- executable with `-u` or `-s` options - `+5` points
- executable with `-u` and `-s` options - `+6` points

You can get `+1` extra point:
- if results/links from search engine can be accessed (using your CLI);
- for implementing HTTP request redirects

You can get `+2` extra points:
- for implementing an HTTP cache mechanism;
- for implementing content negotiation e.g. by accepting and handling both JSON and HTML content types.

## Hints

- Before opting for some language, make sure you have the right tools: CLI parser, HTML/JSON parser, support for TCP sockets;
- For CLI you can use built-in libraries or even Bash built-in [getopts](https://wiki.bash-hackers.org/howto/getopts_tutorial);
- Use third-party libraries for parsing HTML and presenting it;
- While developing, you can launch a local server using `python3 -m http.server` to test & debug the app.
- For HTTP cache you'll need either an in-memory store or file access.
- To avoid `if-else`s in content negotiation, use your knowledge of OOP.
- `<search-term>` can either be a single word or all words following `-s` argument.
