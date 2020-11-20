Prompt
======

Write a server that acts as a bit.ly-like URL shortener. The primary interface should be a JSON API
that allows the following:

 * Create a random short link for arbitrary URLs, e.g., bit.ly/2FhfhXh
 * The same URL should always generate the same random short link
 * Allow creating custom short links to arbitrary URLs, e.g., bit.ly/my-custom-link
 * Multiple custom short links may map to the same URL
 * Provide a route for returning stats on a given short link, including:
   - When the short link was created
   - How many times the short link has been visited total
   - A histogram of number of visits to the short link per day
 * Of course, the server itself should handle redirecting short links to the URLs it creates

Everything else is up to you: the routes for the API, what its parameters and return values are, how
it handles errors. Of course, I will be happy to talk any of these things out, but you are empowered
to make whatever design decisions you like (and ideally explain them!).


TODO
----

 * item 1
 * item 2


DONE
----

 * done 1
 * done 2


# Local Variables:
# mode: rst
# End:

