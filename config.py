def revise_bashrc():
    bash_filename = "~/.bashrc"

    with open(bash_filename, 'r') as bashrc:
        txt = bashrc.read()

    if "Anaconda3/etc/profile.d/conda.sh" not in txt:
        txt += '\n. ~/Anaconda3/etc/profile.d/conda.sh\n'

        with open(bash_filename, 'w') as bashrc:
            bashrc.write(txt)
