# !/bin/zsh

# load .env file
if [ -f .env ]; then
  export $(grep . .env | sed 's/#.*//g' | xargs)
fi
