let
    nixpkgs = https://nixos.org/releases/nixpkgs/nixpkgs-16.03pre74770.2b7b3aa//nixexprs.tar.xz;
    pkgs = import (fetchTarball nixpkgs) {};
    /*pkgs = import <nixpkgs> {inherit crossSystem;};*/
    stdenv = pkgs.stdenv;
    pythonPackages = pkgs.callPackage ./python.nix {
        pythonPackages = pkgs.python35Packages;
    };
in rec {
    main = pythonPackages.buildPythonPackage rec {
        name = "ksurobot";
        version = "0.1.0";
        src = ../.;

        configurePhase = ''
            make
        '';

        /*makeFlagsArray=[ "PREFIX=\${out}" ];*/

        propagatedBuildInputs = with pythonPackages; [ python websockets six setproctitle rpigpio ptpython ];
    };
}
