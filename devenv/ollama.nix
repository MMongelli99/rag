{pkgs, ...}: {
  packages = with pkgs; [ollama];
  processes.ollama.exec = "echo 'running ollama...'";
  tasks = {
    "ollama:setup" = {
      exec = "ollama serve";
      before = ["devenv:processes:ollama"];
    };
    "ollama:cleanup" = {
      exec = "pkill ollama";
      after = ["devenv:processes:ollama"];
    };
  };
}
