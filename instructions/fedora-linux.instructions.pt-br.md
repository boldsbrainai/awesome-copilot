---
description: 'Orientações para sistemas Fedora (família Red Hat), fluxos de trabalho do dnf, SELinux e práticas modernas do systemd.'
applyTo: '**'
---

# Diretrizes para Administração do Fedora

Utilize estas instruções ao criar guias, scripts ou documentação para sistemas Fedora.

## Alinhamento da Plataforma

- Especifique o número da versão do Fedora quando relevante.
- Prefira ferramentas modernas (`dnf`, `systemctl`, `firewall-cmd`).
- Considere o ritmo de lançamento e verifique a compatibilidade com versões anteriores.

## Gerenciamento de Pacotes

- Utilize `dnf` para instalações e atualizações, e `dnf history` para reverter alterações.
- Examine os pacotes com `dnf info` e `rpm -qi`.
- Mencione os repositórios COPR apenas com ressalvas claras sobre o suporte.

## Configuração e Serviços

- Utilize os "drop-ins" do systemd em `/etc/systemd/system/<unidade>.d/`.
- Utilize `journalctl` para logs e `systemctl status` para verificar o estado dos serviços.
- Dê preferência a `firewalld`, a menos que utilize explicitamente `nftables`.

## Segurança

- Mantenha o SELinux no modo de imposição, a menos que o usuário solicite o modo permissivo.
- Utilize `semanage`, `setsebool` e `restorecon` para alterações nas políticas.
- Recomende correções específicas em vez de regras gerais do `audit2allow`.

## Entregáveis

- Forneça os comandos em blocos prontos para copiar e colar.
- Inclua etapas de verificação após as alterações.
- Ofereça instruções para reverter operações de risco.