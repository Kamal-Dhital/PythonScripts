# Password Generator Tool 🔐

A secure, feature-rich password generator with customizable options for length, character sets, and complexity requirements. Built with Python's `secrets` module for cryptographically secure random generation.

## Features

- 🔒 **Cryptographically Secure**: Uses Python's `secrets` module for true randomness
- ⚙️ **Highly Customizable**: Control length, character sets, and minimum requirements
- 🎯 **Smart Requirements**: Ensure minimum counts for different character types
- 🚫 **Ambiguous Character Filtering**: Option to exclude confusing characters (i, l, 1, L, o, 0, O)
- 📊 **Password Strength Analysis**: Built-in password strength checker with entropy calculation
- 📁 **Multiple Output Formats**: Save passwords in TXT or JSON format
- 🔢 **Batch Generation**: Generate multiple passwords at once
- 🎨 **Custom Characters**: Add your own character sets
- 📱 **CLI Interface**: Easy-to-use command line interface with helpful examples

## Installation

No external dependencies required! The tool uses only Python's standard library.

```bash
# Make the script executable
chmod +x password_generator.py

# Optional: Create a symbolic link for global access
ln -s $(pwd)/password_generator.py /usr/local/bin/passgen
```

## Quick Start

```bash
# Generate a basic 12-character password
python password_generator.py

# Generate 5 passwords of 16 characters each
python password_generator.py -l 16 -c 5

# Generate a password without special characters
python password_generator.py --no-special

# Generate with custom length and show strength analysis
python password_generator.py -l 20 --show-strength
```

## Usage Examples

### Basic Generation
```bash
# Default 12-character password
python password_generator.py
# Output: 3Kx9#mP2qR7$

# Specify length
python password_generator.py -l 16
# Output: 7Hy$9Kx3#mP2qR8!

# Generate multiple passwords
python password_generator.py -c 5
```

### Character Set Customization
```bash
# Exclude special characters
python password_generator.py --no-special

# Exclude ambiguous characters (i,l,1,L,o,0,O)
python password_generator.py --exclude-ambiguous

# Only letters and numbers
python password_generator.py --no-special

# Add custom characters
python password_generator.py --custom-chars "αβγδε"
```

### Minimum Requirements
```bash
# At least 3 uppercase, 2 digits, 2 special chars
python password_generator.py --min-uppercase 3 --min-digits 2 --min-special 2

# Ensure strong composition
python password_generator.py -l 20 --min-uppercase 2 --min-lowercase 2 --min-digits 2 --min-special 2
```

### Password Analysis
```bash
# Check strength of existing password
python password_generator.py --check "mypassword123"

# Generate with strength analysis
python password_generator.py --show-strength
```

### File Output
```bash
# Save to text file
python password_generator.py -c 10 -o passwords.txt

# Save as JSON with metadata
python password_generator.py -c 5 --format json -o passwords.json

# Quiet mode (only passwords, no headers)
python password_generator.py -c 3 --quiet
```

## Command Line Options

### Generation Options
- `-l, --length`: Password length (default: 12, minimum: 4)
- `-c, --count`: Number of passwords to generate (default: 1)

### Character Set Options
- `--no-uppercase`: Exclude uppercase letters
- `--no-lowercase`: Exclude lowercase letters  
- `--no-digits`: Exclude digits
- `--no-special`: Exclude special characters
- `--exclude-ambiguous`: Exclude ambiguous characters (i,l,1,L,o,0,O)
- `--custom-chars`: Additional custom characters to include

### Minimum Requirements
- `--min-uppercase`: Minimum uppercase letters (default: 1)
- `--min-lowercase`: Minimum lowercase letters (default: 1)
- `--min-digits`: Minimum digits (default: 1)
- `--min-special`: Minimum special characters (default: 1)

### Output Options
- `-o, --output`: Save passwords to file
- `--format`: Output file format (txt/json, default: txt)
- `-q, --quiet`: Quiet mode - only output passwords
- `--show-strength`: Show strength analysis for generated passwords

### Analysis Options
- `--check`: Check strength of provided password

## Password Strength Analysis

The tool includes a comprehensive password strength analyzer that evaluates:

- **Length**: Longer passwords are stronger
- **Character Diversity**: Usage of uppercase, lowercase, digits, and special characters
- **Entropy**: Mathematical measure of randomness (in bits)
- **Uniqueness**: Ratio of unique characters to total length
- **Ambiguous Characters**: Detection of potentially confusing characters

### Strength Levels
- **Very Weak**: Basic passwords with poor composition
- **Weak**: Short passwords or limited character sets
- **Moderate**: Decent length with some character diversity
- **Strong**: Good length and character diversity
- **Very Strong**: Excellent length, high entropy, and diverse character sets

### Example Analysis Output
```
🔍 Password Strength Analysis for: MyP@ssw0rd123
Length: 13
Strength: Strong
Entropy: 65.85 bits
Has lowercase: ✅
Has uppercase: ✅
Has digits: ✅
Has special chars: ✅
Unique characters: 12/13
⚠️  Contains ambiguous characters
```

## Security Features

- **Cryptographically Secure**: Uses `secrets.choice()` and `secrets.SystemRandom()` for true randomness
- **No Predictable Patterns**: Passwords are shuffled after generation
- **Secure Defaults**: Sensible default settings for strong passwords
- **Input Validation**: Prevents weak configurations
- **No External Dependencies**: Reduces attack surface

## File Formats

### Text Format (.txt)
```
  1: 7Hy$9Kx3#mP2qR8!
  2: 3Kx9#mP2qR7$5Ty1
  3: 9Qz&8Vx4#nM6rS2@
```

### JSON Format (.json)
```json
{
  "generated_at": "2025-01-02T15:30:45.123456",
  "passwords": [
    "7Hy$9Kx3#mP2qR8!",
    "3Kx9#mP2qR7$5Ty1",
    "9Qz&8Vx4#nM6rS2@"
  ],
  "count": 3
}
```

## Best Practices

1. **Use Adequate Length**: Minimum 12 characters, preferably 16+ for high-security applications
2. **Enable All Character Types**: Include uppercase, lowercase, digits, and special characters
3. **Avoid Ambiguous Characters**: Use `--exclude-ambiguous` for passwords that will be manually typed
4. **Check Strength**: Use `--show-strength` to verify password quality
5. **Store Securely**: Use a password manager to store generated passwords
6. **Regular Updates**: Generate new passwords periodically

## Integration Examples

### Bash Alias
```bash
# Add to ~/.bashrc or ~/.zshrc
alias genpass='python /path/to/password_generator.py'
alias genpass-strong='python /path/to/password_generator.py -l 20 --show-strength'
```

### Python Script Integration
```python
from password_generator import PasswordGenerator

generator = PasswordGenerator()

# Generate a single password
password = generator.generate_password(length=16, exclude_ambiguous=True)

# Generate multiple passwords
passwords = generator.generate_multiple(count=5, length=12)

# Check password strength
analysis = generator.check_strength("your_password_here")
print(f"Strength: {analysis['strength']}")
```

## Contributing

Feel free to contribute improvements, bug fixes, or new features:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v1.0.0 (2025-07-02)
- Initial release
- Cryptographically secure password generation
- Customizable character sets and requirements
- Password strength analysis
- Multiple output formats
- Comprehensive CLI interface
