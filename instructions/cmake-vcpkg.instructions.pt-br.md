---
description: 'Configuração de projetos em C++ e gerenciamento de pacotes'
applyTo: '**/*.cmake, **/CMakeLists.txt, **/*.cpp, **/*.h, **/*.hpp'
---

Este projeto utiliza o vcpkg no modo manifest. Tenha isso em mente ao fornecer sugestões para o vcpkg. Não forneça sugestões como "vcpkg install library", pois elas não funcionarão como esperado.
Se possível, prefira definir variáveis de cache e outros elementos através de CMakePresets.json.
Forneça informações sobre quaisquer políticas do CMake que possam afetar variáveis do CMake sugeridas ou mencionadas.
Este projeto precisa ser multiplataforma e compatível com vários compiladores, incluindo MSVC, Clang e GCC.
Ao fornecer exemplos do OpenCV que utilizam o sistema de arquivos para ler arquivos, utilize sempre caminhos absolutos em vez de nomes de arquivos ou caminhos relativos. Por exemplo, use `video.open("C:/project/file.mp4")`, e não `video.open("file.mp4")`.