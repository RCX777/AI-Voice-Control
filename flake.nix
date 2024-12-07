{
  inputs = {
    nixpkgs.url      = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url  = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        python = pkgs.python311;
      in with pkgs;
      {
        devShells.default = mkShell {
          buildInputs = [
            python
          ];
          shellHook = ''
            VENV=.venv

            if test ! -d $VENV; then
              python3.11 -m venv $VENV
            fi
            pip install --upgrade pip
            . ./$VENV/bin/activate
            export PYTHONPATH=`pwd`/$VENV/${python.sitePackages}/:$PYTHONPATH
            pip install -r app/requirements.txt
          '';
          postShellHook = ''
            ln -sf ${python.sitePackages}/* ./.venv/lib/python3.11/site-packages
          '';
        };
      }
    );
}

