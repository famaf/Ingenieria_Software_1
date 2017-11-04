#!/bin/bash


if [ ! $# == 1 ]; then
    echo "you must provide the name of virtualenv"
fi



function download_virtualenv {
    sudo pip install virtualenvwrapper
}

function find_virtualenvwrapper {
   # no consistent way to find 'virtualenvwrapper.sh', so try various methods
   # is it directly available in the path?
   virtualenvwrapper_path=$(which virtualenvwrapper.sh)
   if [ $? -eq 0 ]; then
      return
   fi
   # nope; how about something that looks like it in our path?
   # http://stackoverflow.com/questions/948008/linux-command-to-list-all-available-commands-and-aliases
   virtualenvwrapper_cmd=$(compgen -ac | grep -i 'virtualenvwrapper\.sh' | sort | uniq | head -1)
   if [ -n "$virtualenvwrapper_cmd" ]; then
      virtualenvwrapper_path=$(which $virtualenvwrapper_cmd)
      if [ $? -eq 0 ]; then
         return
      fi
   fi
   # still not; Debubuntu puts it in /etc/bash_completion.d
   virtualenvwrapper_path='/etc/bash_completion.d/virtualenvwrapper'
   if [ -e "$virtualenvwrapper_path" ]; then
      return
   fi
   # any other methods to find virtualenvwrapper can be added here
   echo "unable to find virtualenvwrapper.sh or anything that looks like it"
   exit 1
}

function install_system_deps {
    echo "Instlling libxml2-dev and libxslt1-dev for lxml package."
    echo "sudo apt-get install libxml2-dev"
    sudo apt-get install libxml2-dev
    echo "sudo apt-get install libxslt1-dev"
    sudo apt-get install libxslt1-dev
    echo "sudo apt-get install python-pip"
    sudo apt-get install python-pip
    echo "sudo apt-get install python-dev"
    sudo apt-get install python-dev
}

if [ $# == 1 ]; then
    
    # Install system deps.
    install_system_deps

    # Download and install the virtualenvwrapper.
    download_virtualenv

    # Fill the virtualenvwrapper_path variable with the path to the virtualenvwrapper.
    find_virtualenvwrapper

    # Create the workon_home if not exists.
    export WORKON_HOME=~/.virtualenvs
    if [ ! -d $WORKON_HOME ]; then
        mkdir $WORKON_HOME
    fi

    # Adding WORKON_HOME=${WORKON_HOME} to ${profile_file}.
    profile_file="$HOME/.bashrc"
    if ! grep -q 'WORKON_HOME=' "${profile_file}" ; then
        echo "Adding WORKON_HOME=${WORKON_HOME} to ${profile_file}"
        echo "export WORKON_HOME=${WORKON_HOME}" >> "${profile_file}"
    fi

    # Adding source ${find_virtualenvwrapper} to ${profile_file}.
    if ! grep -q "${virtualenvwrapper_path}" "${profile_file}" ; then
        echo "source ${virtualenvwrapper_path}" >> "${profile_file}"
    fi

    # Reload .bashrc.
    echo "Reloading bashrc..."
    source ~/.bashrc

    # Create the virtualenv PROCenv and install the requeriments on it.
    mkvirtualenv -a ./ -r requeriments.txt ${1}
    cd ..

    # Adding colors to virtualenv console.
    virtual_env_hook="$VIRTUALENVWRAPPER_HOOK_DIR/postactivate"
    if ! grep -q "PS1=" "${virtual_env_hook}" ; then
        echo "PS1=\"\[\e[0;31m\](\`basename \\\"\$VIRTUAL_ENV\\\"\`)\n\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ \"" >> "${virtual_env_hook}"
    fi

    # Set the virtualenv.
    workon ${1}

    # Add current dir to python path for this virtualenv.
    add2virtualenv .

    # Deactivate the virtualenv.
    deactivate

    # Set the virtualenv.
    workon ${1}
fi



