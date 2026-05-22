"""Unified Socaity CLI: auth, SDK services, and APIPod deployment tooling."""

from __future__ import annotations

import argparse

from socaity.cli_auth import run_login, run_whoami
from socaity.cli_apipod import run_build, run_scan, run_start
from socaity.core.credentials import clear_credentials, require_credentials
from socaity.core.socaity_service_registry import SocaityServiceRegistry

# Mirror apipod.common.constants (avoid importing apipod until a deploy command runs).
_ORCHESTRATOR_CHOICES = ("local", "socaity")
_COMPUTE_CHOICES = ("dedicated", "serverless")
_PROVIDER_CHOICES = ("auto", "localhost", "socaity", "runpod", "scaleway", "azure")


def _add_apipod_config_args(parser: argparse.ArgumentParser) -> None:
    orchestrator_choices = _ORCHESTRATOR_CHOICES
    compute_choices = _COMPUTE_CHOICES
    provider_choices = _PROVIDER_CHOICES
    group = parser.add_argument_group("deployment configuration")
    group.add_argument(
        "--orchestrator",
        choices=orchestrator_choices,
        default="local",
        help=f"Orchestration platform (default: local). Options: {', '.join(orchestrator_choices)}",
    )
    group.add_argument(
        "--compute",
        choices=compute_choices,
        default="dedicated",
        help=f"Compute type (default: dedicated). Options: {', '.join(compute_choices)}",
    )
    group.add_argument(
        "--provider",
        choices=provider_choices,
        default="localhost",
        help=f"Infrastructure provider (default: localhost). Options: {', '.join(provider_choices)}",
    )
    group.add_argument("--region", default=None, help="Deployment region (provider-specific)")


def _run_install(service_name: str) -> None:
    require_credentials()
    registry = SocaityServiceRegistry()
    if service_name.lower() == "all":
        print("Installing all available services...")
        registry.install_all()
    else:
        print(f"Installing service: {service_name}...")
        registry.install_service(service_name)


def _run_update() -> None:
    require_credentials()
    print("Checking for service updates...")
    SocaityServiceRegistry().update_package()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Socaity SDK, authentication, and APIPod deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  socaity login
  socaity install black-forest-labs/flux-schnell
  socaity update
  socaity scan
  socaity build main.py --provider runpod
  socaity start --compute serverless --provider runpod
        """,
    )
    parser.add_argument(
        "-i", "--install",
        metavar="SERVICE",
        help="Install an AI service (requires login)",
    )

    subparsers = parser.add_subparsers(dest="command")

    login_parser = subparsers.add_parser("login", help="Authenticate via browser and save credentials")
    login_parser.add_argument("--no-browser", action="store_true", help="Do not open a browser automatically")
    login_parser.add_argument("--timeout", type=int, default=300, help="Seconds to wait for browser login")
    login_parser.add_argument(
        "--backend-url",
        default=None,
        help="API base URL (default: SOCAITY_BACKEND_URL or https://webapi.socaity.ai)",
    )
    login_parser.add_argument(
        "--frontend-url",
        default=None,
        help="Web UI base URL for sign-in (default: SOCAITY_FRONTEND_URL or https://www.socaity.ai)",
    )

    subparsers.add_parser("logout", help="Remove stored credentials")
    subparsers.add_parser("whoami", help="Show logged-in user")

    install_parser = subparsers.add_parser("install", help="Install an AI service")
    install_parser.add_argument("service_name", help='Service name, ID, or "all"')

    subparsers.add_parser("update", help="Sync installed services with the platform")

    subparsers.add_parser("scan", help="Scan project and generate apipod.json (requires apipod)")

    build_parser = subparsers.add_parser("build", help="Build deployment container (requires apipod)")
    build_parser.add_argument("file", nargs="?", default=None, help="Entry Python file (e.g. main.py)")
    _add_apipod_config_args(build_parser)

    start_parser = subparsers.add_parser("start", help="Start APIPod service locally (requires apipod)")
    _add_apipod_config_args(start_parser)
    start_parser.add_argument("--host", default=None, help="Host to bind (default: 0.0.0.0)")
    start_parser.add_argument("--port", type=int, default=None, help="Port to bind (default: 8000)")

    args = parser.parse_args(argv)

    if args.install:
        _run_install(args.install)
        return

    if args.command == "login":
        run_login(
            no_browser=args.no_browser,
            timeout=args.timeout,
            backend_url=args.backend_url,
            frontend_url=args.frontend_url,
        )
        return

    if args.command == "logout":
        if clear_credentials():
            print("Logged out. Credentials removed.")
        else:
            print("Not logged in.")
        return

    if args.command == "whoami":
        run_whoami()
        return

    if args.command == "install":
        _run_install(args.service_name)
        return

    if args.command == "update":
        _run_update()
        return

    if args.command == "scan":
        require_credentials()
        run_scan()
        return

    if args.command == "build":
        require_credentials()
        run_build(
            args.file,
            orchestrator=args.orchestrator,
            compute=args.compute,
            provider=args.provider,
            region=args.region,
        )
        return

    if args.command == "start":
        require_credentials()
        run_start(
            orchestrator=args.orchestrator,
            compute=args.compute,
            provider=args.provider,
            region=args.region,
            host=args.host,
            port=args.port,
        )
        return

    parser.print_help()


if __name__ == "__main__":
    main()
