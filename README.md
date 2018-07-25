mtriv is a multi-user trivia game/chat program with trivia plugin. It's written using python3 and sockets, nothing more. The client included will work on most
standard unix systems and on most standard unix terminals. For the trivia functionality, send !startq in chat. This pulls a random question from a file loaded into memory when the server starts up. The server can read from a format such that the first digit in the question string is an integer of any length which is followed by a period. Both the question and answer are followed by a colon(:) unless it is the last question, in which case the answer doesn't need to be followed up with one.
<br/>
Ex: "99. What is 1 + 1?":"2"
<br/>
Ex: "99. What is 1 + 1?":"2":"100. What is 1 + 2?":"3"
 <br/>
There's a file in the repo, paste2qdoc, that I wrote to convert strings in one specific format to the one the program reads. This could help in adding more questions in bulk.

