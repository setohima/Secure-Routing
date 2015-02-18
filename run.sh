#!/bin/bash
javac GossipServer.java
gnome-terminal --tab -e "java GossipServer" --tab -e "pwd"
