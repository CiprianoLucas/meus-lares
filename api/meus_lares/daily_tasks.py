from subprocess import run

def run_django_command(command):
    result = run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error executing command '{command}': {result.stderr}")

def main():
    base_command = '/usr/local/bin/poetry run python manage.py '
    commands = [
        base_command + 'getcelescinvoices',
    ]

    for command in commands:
        run_django_command(command)

if __name__ == '__main__':
    main()
