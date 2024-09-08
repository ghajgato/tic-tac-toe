# tic-tac-toe

### Docker
`docker build -f Dockerfile --tag xo .`


`xhost +local:docker`


```
docker run -e DISPLAY=$DISPLAY \
           -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
           -v $HOME/.Xauthority:/root/.Xauthority:rw \
           --net=host \
           --rm -it xo
```
