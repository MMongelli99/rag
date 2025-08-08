{pkgs, ...}: {
  packages = with pkgs; [starship];
  enterShell = ''
    eval "$(starship init bash)"
  '';
}
