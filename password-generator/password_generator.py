#!/usr/bin/env python3
"""
Password Generator Tool
A secure password generator with customizable options for length, character sets, and complexity.
"""

import argparse
import secrets
import string
import sys
import json
import os
from typing import List, Dict, Any


class PasswordGenerator:
    """A secure password generator with various customization options."""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()-_+=[]{}|;:,.<>?"
        self.ambiguous_chars = "il1Lo0O"
    
    def generate_password(
        self,
        length: int = 12,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True,
        exclude_ambiguous: bool = False,
        custom_chars: str = "",
        min_uppercase: int = 1,
        min_lowercase: int = 1,
        min_digits: int = 1,
        min_special: int = 1
    ) -> str:
        """
        Generate a secure password with specified criteria.
        
        Args:
            length: Password length (minimum 4)
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters (i, l, 1, L, o, 0, O)
            custom_chars: Additional custom characters to include
            min_uppercase: Minimum number of uppercase letters
            min_lowercase: Minimum number of lowercase letters
            min_digits: Minimum number of digits
            min_special: Minimum number of special characters
            
        Returns:
            Generated password string
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character set
        char_pool = ""
        required_chars = []
        
        if include_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            char_pool += chars
            required_chars.extend([secrets.choice(chars) for _ in range(min_lowercase)])
        
        if include_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            char_pool += chars
            required_chars.extend([secrets.choice(chars) for _ in range(min_uppercase)])
        
        if include_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.ambiguous_chars)
            char_pool += chars
            required_chars.extend([secrets.choice(chars) for _ in range(min_digits)])
        
        if include_special:
            chars = self.special_chars
            char_pool += chars
            required_chars.extend([secrets.choice(chars) for _ in range(min_special)])
        
        if custom_chars:
            char_pool += custom_chars
        
        if not char_pool:
            raise ValueError("No character types selected")
        
        # Check if minimum requirements can be met
        total_min_chars = len(required_chars)
        if total_min_chars > length:
            raise ValueError(f"Minimum character requirements ({total_min_chars}) exceed password length ({length})")
        
        # Generate remaining characters
        remaining_length = length - total_min_chars
        password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def generate_multiple(self, count: int, **kwargs) -> List[str]:
        """Generate multiple passwords with the same criteria."""
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def check_strength(self, password: str) -> Dict[str, Any]:
        """
        Analyze password strength and provide feedback.
        
        Args:
            password: Password to analyze
            
        Returns:
            Dictionary containing strength analysis
        """
        analysis = {
            "length": len(password),
            "has_lowercase": any(c in self.lowercase for c in password),
            "has_uppercase": any(c in self.uppercase for c in password),
            "has_digits": any(c in self.digits for c in password),
            "has_special": any(c in self.special_chars for c in password),
            "has_ambiguous": any(c in self.ambiguous_chars for c in password),
            "unique_chars": len(set(password)),
            "entropy": 0,
            "strength": "Very Weak"
        }
        
        # Calculate entropy
        char_pool_size = 0
        if analysis["has_lowercase"]:
            char_pool_size += 26
        if analysis["has_uppercase"]:
            char_pool_size += 26
        if analysis["has_digits"]:
            char_pool_size += 10
        if analysis["has_special"]:
            char_pool_size += len(self.special_chars)
        
        if char_pool_size > 0:
            import math
            analysis["entropy"] = len(password) * math.log2(char_pool_size)
        
        # Determine strength
        score = 0
        if analysis["length"] >= 8:
            score += 1
        if analysis["length"] >= 12:
            score += 1
        if analysis["has_lowercase"]:
            score += 1
        if analysis["has_uppercase"]:
            score += 1
        if analysis["has_digits"]:
            score += 1
        if analysis["has_special"]:
            score += 1
        if analysis["unique_chars"] >= len(password) * 0.8:  # 80% unique characters
            score += 1
        if analysis["entropy"] >= 60:
            score += 1
        
        if score <= 2:
            analysis["strength"] = "Very Weak"
        elif score <= 4:
            analysis["strength"] = "Weak"
        elif score <= 6:
            analysis["strength"] = "Moderate"
        elif score <= 7:
            analysis["strength"] = "Strong"
        else:
            analysis["strength"] = "Very Strong"
        
        return analysis


def save_passwords_to_file(passwords: List[str], filename: str, format_type: str = "txt"):
    """Save passwords to a file in specified format."""
    if format_type == "json":
        data = {
            "generated_at": __import__('datetime').datetime.now().isoformat(),
            "passwords": passwords,
            "count": len(passwords)
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    else:  # txt format
        with open(filename, 'w') as f:
            for i, password in enumerate(passwords, 1):
                f.write(f"{i:3d}: {password}\n")
    
    print(f"✅ Passwords saved to {filename}")


def main():
    """Main function to handle command line arguments and generate passwords."""
    parser = argparse.ArgumentParser(
        description="Generate secure passwords with customizable options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Generate a 12-character password
  %(prog)s -l 16 -c 5              # Generate 5 passwords of 16 characters each
  %(prog)s -l 20 --no-special      # Generate without special characters
  %(prog)s --exclude-ambiguous     # Exclude ambiguous characters (i,l,1,L,o,0,O)
  %(prog)s --check "mypassword123" # Check password strength
  %(prog)s -l 15 -o passwords.txt  # Save to file
        """
    )
    
    # Generation options
    parser.add_argument("-l", "--length", type=int, default=12,
                       help="Password length (default: 12, minimum: 4)")
    parser.add_argument("-c", "--count", type=int, default=1,
                       help="Number of passwords to generate (default: 1)")
    
    # Character set options
    parser.add_argument("--no-uppercase", action="store_true",
                       help="Exclude uppercase letters")
    parser.add_argument("--no-lowercase", action="store_true",
                       help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true",
                       help="Exclude digits")
    parser.add_argument("--no-special", action="store_true",
                       help="Exclude special characters")
    parser.add_argument("--exclude-ambiguous", action="store_true",
                       help="Exclude ambiguous characters (i,l,1,L,o,0,O)")
    parser.add_argument("--custom-chars", type=str, default="",
                       help="Additional custom characters to include")
    
    # Minimum requirements
    parser.add_argument("--min-uppercase", type=int, default=1,
                       help="Minimum uppercase letters (default: 1)")
    parser.add_argument("--min-lowercase", type=int, default=1,
                       help="Minimum lowercase letters (default: 1)")
    parser.add_argument("--min-digits", type=int, default=1,
                       help="Minimum digits (default: 1)")
    parser.add_argument("--min-special", type=int, default=1,
                       help="Minimum special characters (default: 1)")
    
    # Output options
    parser.add_argument("-o", "--output", type=str,
                       help="Save passwords to file")
    parser.add_argument("--format", choices=["txt", "json"], default="txt",
                       help="Output file format (default: txt)")
    
    # Analysis option
    parser.add_argument("--check", type=str,
                       help="Check strength of provided password")
    
    # Display options
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="Quiet mode - only output passwords")
    parser.add_argument("--show-strength", action="store_true",
                       help="Show strength analysis for generated passwords")
    
    args = parser.parse_args()
    
    generator = PasswordGenerator()
    
    # Check password strength if requested
    if args.check:
        analysis = generator.check_strength(args.check)
        if not args.quiet:
            print(f"\n🔍 Password Strength Analysis for: {args.check}")
            print(f"Length: {analysis['length']}")
            print(f"Strength: {analysis['strength']}")
            print(f"Entropy: {analysis['entropy']:.2f} bits")
            print(f"Has lowercase: {'✅' if analysis['has_lowercase'] else '❌'}")
            print(f"Has uppercase: {'✅' if analysis['has_uppercase'] else '❌'}")
            print(f"Has digits: {'✅' if analysis['has_digits'] else '❌'}")
            print(f"Has special chars: {'✅' if analysis['has_special'] else '❌'}")
            print(f"Unique characters: {analysis['unique_chars']}/{analysis['length']}")
            if analysis['has_ambiguous']:
                print("⚠️  Contains ambiguous characters")
        return
    
    try:
        # Generate passwords
        passwords = generator.generate_multiple(
            count=args.count,
            length=args.length,
            include_uppercase=not args.no_uppercase,
            include_lowercase=not args.no_lowercase,
            include_digits=not args.no_digits,
            include_special=not args.no_special,
            exclude_ambiguous=args.exclude_ambiguous,
            custom_chars=args.custom_chars,
            min_uppercase=args.min_uppercase if not args.no_uppercase else 0,
            min_lowercase=args.min_lowercase if not args.no_lowercase else 0,
            min_digits=args.min_digits if not args.no_digits else 0,
            min_special=args.min_special if not args.no_special else 0
        )
        
        # Display passwords
        if not args.quiet:
            print(f"\n🔐 Generated {len(passwords)} password(s):")
            print("-" * 50)
        
        for i, password in enumerate(passwords, 1):
            if args.quiet:
                print(password)
            else:
                print(f"{i:3d}: {password}")
                
                if args.show_strength:
                    analysis = generator.check_strength(password)
                    print(f"     Strength: {analysis['strength']} (Entropy: {analysis['entropy']:.1f} bits)")
        
        # Save to file if requested
        if args.output:
            save_passwords_to_file(passwords, args.output, args.format)
        
        if not args.quiet:
            print(f"\n💡 Tip: Use --show-strength to see password strength analysis")
            
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation cancelled by user", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
