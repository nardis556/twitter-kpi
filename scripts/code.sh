#!bin/bash

function deps() {
    bash -c 'sudo apt update && sudo apt upgrade -y'
    bash -c 'sudo apt install curl git gcc make make build-essential \
            libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev \
            wget curl llvm libncursesw5-dev xz-utils tk-dev libxml2-dev \
            libxmlsec1-dev libffi-dev liblzma-dev -y'
    bash -c 'sudo apt upgrade -y'
}

function code() {
    bash -c 'curl -fsSL https://code-server.dev/install.sh | sh'
    bash -c 'sudo systemctl enable --now code-server@$USER'
}


function nvm() {
    bash -c 'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash'
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
}

function pyenv() {
    bash -c 'git clone https://github.com/pyenv/pyenv.git ~/.pyenv'
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
}

echo 'Would you like to install pyenv? Enter: y/n'
read pyenvCond

echo 'Would you like to install nvm? Enter: y/n'
read nvmCond

echo 'Would you like to install code-server? Enter: y/n'
read codeCond

echo 'installing dependencies'
deps

if [ $pyenvCond == 'y' -o $pyenvCond == 'Y' ]
then
  echo "installing pyenv"
  pyenv
fi
if [ $nvmCond == 'y' -o $nvmCond == 'Y' ]
then
  echo "installing nvm"
  nvm
  bash -c 'nvm install-latest-npm'
fi
if [ $codeCond == 'y' -o $codeCond == 'Y' ]
then
  echo "installing code-server"
  code
fi

exec bash
echo "Done"
