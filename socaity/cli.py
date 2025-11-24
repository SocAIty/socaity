import argparse
from socaity.core.socaity_service_manager import SocaityServiceManager


def main():
    parser = argparse.ArgumentParser(description="Socaity SDK Manager")
    
    # Create subparsers for different commands if we want to expand later, 
    # but user requested -install flag style or python -m socaity install
    
    # However, standard python CLI usually uses subcommands (like pip install).
    # The user requested:
    # - "socaity -install ai_service_name_or_id"
    # - "socaity -i ai_service_name_or_id"
    # - "socaity -i all"
    # - "python -m socaity install ai_service_name_or_id"
    
    # So we need to handle both arguments.
    
    # We can use add_argument for -i/-install
    parser.add_argument("-i", "--install", help="Install a specific AI service or 'all'", type=str)
    
    # We also need to handle the subcommand 'install' for "python -m socaity install ..."
    subparsers = parser.add_subparsers(dest='command')
    install_parser = subparsers.add_parser('install', help='Install an AI service')
    install_parser.add_argument('service_name', help='Name or ID of the service to install (or "all")')

    args = parser.parse_args()
    
    service_manager = SocaityServiceManager()
    
    target_service = None
    
    if args.install:
        target_service = args.install
    elif args.command == 'install' and args.service_name:
        target_service = args.service_name
        
    if target_service:
        if target_service.lower() == "all":
            print("Installing all available services...")
            service_manager.install_all()
        else:
            print(f"Installing service: {target_service}...")
            service_manager.install_service(target_service)
    else:
        # Default behavior if run without arguments? 
        # Maybe just update/check official?
        # "By default the package will NOT install all models. It will only update / install the official models."
        print("Updating official packages...")
        service_manager.update_package()


if __name__ == "__main__":
    main()
