{
  vim = {
    treesitter.enable = true;
    lsp = {
      enable = true;
      formatOnSave = true;
      inlayHints.enable = true;
    };
    languages = {
      enableExtraDiagnostics = true;
      enableFormat = true;
      enableTreesitter = true;

      nix.enable = true;
      ts.enable = true;
      tailwind.enable = true;
      python.enable = true;
      sql.enable = true;
      bash.enable = true;
      markdown.enable = true;
    };
  };
}
