{
  inputs,
  pkgs,
  ...
}: {
  packages = let
    customNeovim =
      (inputs.nvf.lib.neovimConfiguration {
        inherit pkgs;
        modules = [
          {
            imports = [
              ./frills.nix
              ./languages.nix
              ./fzflua.nix
              ./git.nix
            ];
            vim.undoFile.enable = true;
          }
        ];
      }).neovim;
  in [customNeovim];
}
