#!/usr/bin/env python3
"""
Sistema de Concessionária
Escolha entre interface de terminal ou interface gráfica
"""

import sys
import os

def show_interface_menu():
    """Show interface selection menu"""
    print("=" * 50)
    print("SISTEMA DE CONCESSIONÁRIA")
    print("=" * 50)
    print()
    print("Escolha a interface:")
    print("1. Interface de Terminal")
    print("2. Interface Gráfica (GUI)")
    print("3. Inicializar Base de Dados")
    print("0. Sair")
    print()

def initialize_database():
    """Initialize and seed the database"""
    try:
        from scripts.create_database import create_database
        from scripts.seed_database import seed_database
        
        print("Criando base de dados...")
        create_database()
        
        print("Populando com dados de exemplo...")
        seed_database()
        
        print("Base de dados inicializada com sucesso!")
        input("Pressione Enter para continuar...")
        
    except Exception as e:
        print(f"Erro ao inicializar base de dados: {e}")
        input("Pressione Enter para continuar...")

def main():
    """Main application entry point"""
    while True:
        try:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            show_interface_menu()
            
            choice = input("Escolha uma opção: ").strip()
            
            if choice == '1':
                # Terminal interface
                from terminal_interface import TerminalInterface
                app = TerminalInterface()
                app.run()
                
            elif choice == '2':
                # GUI interface
                try:
                    from gui_interface import GUIInterface
                    app = GUIInterface()
                    app.run()
                except ImportError as e:
                    print(f"Erro ao carregar interface gráfica: {e}")
                    print("Certifique-se de que o tkinter está instalado.")
                    input("Pressione Enter para continuar...")
                
            elif choice == '3':
                # Initialize database
                initialize_database()
                
            elif choice == '0':
                print("Obrigado por usar o Sistema de Concessionária!")
                sys.exit(0)
                
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\nSaindo do sistema...")
            sys.exit(0)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    main()
