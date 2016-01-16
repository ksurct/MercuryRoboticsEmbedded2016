let
    nixpkgs = {
        url=https://nixos.org/releases/nixpkgs/nixpkgs-16.03pre74770.2b7b3aa//nixexprs.tar.xz;
        sha256="03h7zw992rf7n7k3c3xm8ciiws5ry3vs2acpznch36a4vldvbdm5";
    };
    config = {
        packageOverrides = pkgs: rec {
            pythonPackages = pkgs.callPackage ./pythonPackages.nix {};
            python35Packages = pkgs.callPackage ./pythonPackages.nix {pythonPackages=pkgs.python35Packages;};
        };
    };
    system = "armv7l-linux";
    pkgs = import ((import <nixpkgs> {}).fetchzip nixpkgs) {
        inherit config;};
in let {
    body = pkgs.callPackage ./system.nix {inherit ksurobot;};
    ksurobot = pkgs.callPackage ./ksurobot.nix {};
}
