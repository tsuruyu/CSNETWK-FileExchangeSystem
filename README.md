Good morning, sir!

I have attached three client-side codes each for Alice, Bob, and Charlie only for the sole purpose of simulating multiple client instances.

Additionally, due to lack of time, I was not able to put this in the recording. The server can be manually quit by typing "shutdown" on any of the client-side applications, and any client cannot call /dir if the server has shut down. You can verify this manually or by looking at line 47 on any client functions (def dir(): etc.) and line 74 at the server application (condition: shutdown, then server.close).