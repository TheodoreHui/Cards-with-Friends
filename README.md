# Cards-with-Friends
This project is an all-python framework for multiplayer games, made for UCSD SPIS 2020 by Theodore Hui and Nikunj. Both of us started SPIS with no knowledge of Python, with Theo only taking AP CS in high school and Nik a few HTML classes. Using pygame, a small demo game is implemented to showcase client/server relationship. A combination of threading and socket libraries allows for connection and communication between a server script and any number of client scripts. While the default ip is localhost, a port-forwarded connection could theoretically allow for a true online experience, with each player only needing to run the client script. 
## How do multiplayer games work?
Every client connects to a central server, each continuously pinging the server for realtime updates to data in addition to sending any client-side changes to data, in this example cards. The server stores a copy of all the cards in the deck, which is continuously updated in real time to match client decks. When the server detects a change in card position, that position change is sent out to all other clients. This way, when a new client is added, it can be initialized and synced with concurrently running clients, resulting in a shared display between all clients.
## Future additions
### Adding a functional game:
The original idea for this project was for an online version of the cardgame Mao. However, due to time constraints, the end product game was cut short to just a demo.
### How scripts communicate:
 Currently, all data is translated into strings, wrapped in a Pickle library object, then sent via socket. This is horribly inefficient as these strings need to be unpickled, then further decomposed and casted into usable data. The Pickle library does support packaging more complicated objects such as lists and dictionaries, however this was skipped for the sake of simplicity. However, this leads to messy string decomposition and if comparisons, very messy to debug. Also, the fact that this was written to python bars the client from easily becoming embedded in an html website. If this had been done in JavaScript, Flask, Nodejs and Socket.io already exist to easily deliver code to browsers. 
