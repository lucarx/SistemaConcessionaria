import os
import sys
from typing import Optional
from database import DatabaseManager

class TerminalInterface:
    def __init__(self):
        self.db = DatabaseManager()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f"{title:^60}")
        print("=" * 60)
    
    def print_menu(self, title: str, options: list):
        """Print a formatted menu"""
        self.clear_screen()
        self.print_header(title)
        print()
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("0. Voltar/Sair")
        print()
    
    def get_input(self, prompt: str, input_type: type = str, required: bool = True):
        """Get user input with validation"""
        while True:
            try:
                value = input(f"{prompt}: ").strip()
                if not value and required:
                    print("Este campo é obrigatório!")
                    continue
                if not value and not required:
                    return None
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                return value
            except ValueError:
                print(f"Por favor, insira um valor válido ({input_type.__name__})")
            except KeyboardInterrupt:
                print("\nOperação cancelada.")
                return None
    
    def wait_for_enter(self):
        """Wait for user to press Enter"""
        input("\nPressione Enter para continuar...")
    
    def run(self):
        """Main application loop"""
        while self.running:
            self.main_menu()
    
    def main_menu(self):
        """Display main menu"""
        options = [
            "Gerenciar Veículos",
            "Gerenciar Clientes", 
            "Gerenciar Vendas",
            "Gerenciar Funcionários",
            "Relatórios",
            "Buscar Veículos"
        ]
        
        self.print_menu("SISTEMA DE CONCESSIONÁRIA", options)
        
        choice = self.get_input("Escolha uma opção", int, False)
        
        if choice == 1:
            self.vehicle_menu()
        elif choice == 2:
            self.customer_menu()
        elif choice == 3:
            self.sales_menu()
        elif choice == 4:
            self.employee_menu()
        elif choice == 5:
            self.reports_menu()
        elif choice == 6:
            self.search_vehicles()
        elif choice == 0:
            self.running = False
            print("Obrigado por usar o Sistema de Concessionária!")
        else:
            print("Opção inválida!")
            self.wait_for_enter()
    
    def vehicle_menu(self):
        """Vehicle management menu"""
        while True:
            options = [
                "Adicionar Veículo",
                "Listar Veículos",
                "Atualizar Veículo",
                "Remover Veículo"
            ]
            
            self.print_menu("GERENCIAR VEÍCULOS", options)
            choice = self.get_input("Escolha uma opção", int, False)
            
            if choice == 1:
                self.add_vehicle()
            elif choice == 2:
                self.list_vehicles()
            elif choice == 3:
                self.update_vehicle()
            elif choice == 4:
                self.delete_vehicle()
            elif choice == 0:
                break
            else:
                print("Opção inválida!")
                self.wait_for_enter()
    
    def add_vehicle(self):
        """Add a new vehicle"""
        self.clear_screen()
        self.print_header("ADICIONAR VEÍCULO")
        
        brand = self.get_input("Marca")
        model = self.get_input("Modelo")
        year = self.get_input("Ano", int)
        color = self.get_input("Cor")
        price = self.get_input("Preço", float)
        mileage = self.get_input("Quilometragem", int, False) or 0
        fuel_type = self.get_input("Tipo de Combustível (Gasoline/Flex/Diesel)", str, False) or "Gasoline"
        transmission = self.get_input("Transmissão (Manual/Automatic)", str, False) or "Manual"
        
        try:
            vehicle_id = self.db.add_vehicle(brand, model, year, color, price, mileage, fuel_type, transmission)
            print(f"Veículo adicionado com sucesso! ID: {vehicle_id}")
        except Exception as e:
            print(f"Erro ao adicionar veículo: {e}")
        
        self.wait_for_enter()
    
    def list_vehicles(self):
        """List all vehicles"""
        self.clear_screen()
        self.print_header("LISTA DE VEÍCULOS")
        
        vehicles = self.db.get_vehicles()
        
        if not vehicles:
            print("Nenhum veículo encontrado.")
        else:
            print(f"{'ID':<5} {'Marca':<12} {'Modelo':<15} {'Ano':<6} {'Cor':<10} {'Preço':<12} {'Status':<10}")
            print("-" * 80)
            for vehicle in vehicles:
                print(f"{vehicle['id']:<5} {vehicle['brand']:<12} {vehicle['model']:<15} "
                      f"{vehicle['year']:<6} {vehicle['color']:<10} R${vehicle['price']:<11.2f} {vehicle['status']:<10}")
        
        self.wait_for_enter()
    
    def update_vehicle(self):
        """Update vehicle information"""
        self.clear_screen()
        self.print_header("ATUALIZAR VEÍCULO")
        
        vehicle_id = self.get_input("ID do veículo", int)
        vehicle = self.db.get_vehicle_by_id(vehicle_id)
        
        if not vehicle:
            print("Veículo não encontrado!")
            self.wait_for_enter()
            return
        
        print(f"Veículo atual: {vehicle['brand']} {vehicle['model']} {vehicle['year']}")
        print("Deixe em branco para manter o valor atual.")
        
        updates = {}
        
        brand = self.get_input("Nova marca", str, False)
        if brand: updates['brand'] = brand
        
        model = self.get_input("Novo modelo", str, False)
        if model: updates['model'] = model
        
        price_str = self.get_input("Novo preço", str, False)
        if price_str:
            try:
                updates['price'] = float(price_str)
            except ValueError:
                print("Preço inválido!")
        
        status = self.get_input("Novo status (Available/Sold)", str, False)
        if status: updates['status'] = status
        
        if updates:
            if self.db.update_vehicle(vehicle_id, **updates):
                print("Veículo atualizado com sucesso!")
            else:
                print("Erro ao atualizar veículo!")
        else:
            print("Nenhuma alteração realizada.")
        
        self.wait_for_enter()
    
    def delete_vehicle(self):
        """Delete a vehicle"""
        self.clear_screen()
        self.print_header("REMOVER VEÍCULO")
        
        vehicle_id = self.get_input("ID do veículo", int)
        vehicle = self.db.get_vehicle_by_id(vehicle_id)
        
        if not vehicle:
            print("Veículo não encontrado!")
            self.wait_for_enter()
            return
        
        print(f"Veículo: {vehicle['brand']} {vehicle['model']} {vehicle['year']}")
        confirm = self.get_input("Tem certeza que deseja remover? (s/N)", str, False)
        
        if confirm and confirm.lower() == 's':
            if self.db.delete_vehicle(vehicle_id):
                print("Veículo removido com sucesso!")
            else:
                print("Erro ao remover veículo!")
        else:
            print("Operação cancelada.")
        
        self.wait_for_enter()
    
    def customer_menu(self):
        """Customer management menu"""
        while True:
            options = [
                "Adicionar Cliente",
                "Listar Clientes",
                "Atualizar Cliente",
                "Remover Cliente"
            ]
            
            self.print_menu("GERENCIAR CLIENTES", options)
            choice = self.get_input("Escolha uma opção", int, False)
            
            if choice == 1:
                self.add_customer()
            elif choice == 2:
                self.list_customers()
            elif choice == 3:
                self.update_customer()
            elif choice == 4:
                self.delete_customer()
            elif choice == 0:
                break
            else:
                print("Opção inválida!")
                self.wait_for_enter()
    
    def add_customer(self):
        """Add a new customer"""
        self.clear_screen()
        self.print_header("ADICIONAR CLIENTE")
        
        name = self.get_input("Nome")
        email = self.get_input("Email")
        phone = self.get_input("Telefone")
        address = self.get_input("Endereço", str, False) or ""
        cpf = self.get_input("CPF", str, False) or ""
        
        try:
            customer_id = self.db.add_customer(name, email, phone, address, cpf)
            print(f"Cliente adicionado com sucesso! ID: {customer_id}")
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
        
        self.wait_for_enter()
    
    def list_customers(self):
        """List all customers"""
        self.clear_screen()
        self.print_header("LISTA DE CLIENTES")
        
        customers = self.db.get_customers()
        
        if not customers:
            print("Nenhum cliente encontrado.")
        else:
            print(f"{'ID':<5} {'Nome':<20} {'Email':<25} {'Telefone':<15}")
            print("-" * 70)
            for customer in customers:
                print(f"{customer['id']:<5} {customer['name']:<20} {customer['email']:<25} {customer['phone']:<15}")
        
        self.wait_for_enter()
    
    def update_customer(self):
        """Update customer information"""
        self.clear_screen()
        self.print_header("ATUALIZAR CLIENTE")
        
        customer_id = self.get_input("ID do cliente", int)
        customer = self.db.get_customer_by_id(customer_id)
        
        if not customer:
            print("Cliente não encontrado!")
            self.wait_for_enter()
            return
        
        print(f"Cliente atual: {customer['name']} - {customer['email']}")
        print("Deixe em branco para manter o valor atual.")
        
        updates = {}
        
        name = self.get_input("Novo nome", str, False)
        if name: updates['name'] = name
        
        email = self.get_input("Novo email", str, False)
        if email: updates['email'] = email
        
        phone = self.get_input("Novo telefone", str, False)
        if phone: updates['phone'] = phone
        
        if updates:
            if self.db.update_customer(customer_id, **updates):
                print("Cliente atualizado com sucesso!")
            else:
                print("Erro ao atualizar cliente!")
        else:
            print("Nenhuma alteração realizada.")
        
        self.wait_for_enter()
    
    def delete_customer(self):
        """Delete a customer"""
        self.clear_screen()
        self.print_header("REMOVER CLIENTE")
        
        customer_id = self.get_input("ID do cliente", int)
        customer = self.db.get_customer_by_id(customer_id)
        
        if not customer:
            print("Cliente não encontrado!")
            self.wait_for_enter()
            return
        
        print(f"Cliente: {customer['name']} - {customer['email']}")
        confirm = self.get_input("Tem certeza que deseja remover? (s/N)", str, False)
        
        if confirm and confirm.lower() == 's':
            if self.db.delete_customer(customer_id):
                print("Cliente removido com sucesso!")
            else:
                print("Erro ao remover cliente!")
        else:
            print("Operação cancelada.")
        
        self.wait_for_enter()
    
    def sales_menu(self):
        """Sales management menu"""
        while True:
            options = [
                "Registrar Venda",
                "Listar Vendas"
            ]
            
            self.print_menu("GERENCIAR VENDAS", options)
            choice = self.get_input("Escolha uma opção", int, False)
            
            if choice == 1:
                self.add_sale()
            elif choice == 2:
                self.list_sales()
            elif choice == 0:
                break
            else:
                print("Opção inválida!")
                self.wait_for_enter()
    
    def add_sale(self):
        """Add a new sale"""
        self.clear_screen()
        self.print_header("REGISTRAR VENDA")
        
        # Show available vehicles
        available_vehicles = self.db.get_vehicles("Available")
        if not available_vehicles:
            print("Nenhum veículo disponível para venda!")
            self.wait_for_enter()
            return
        
        print("Veículos disponíveis:")
        for vehicle in available_vehicles:
            print(f"ID {vehicle['id']}: {vehicle['brand']} {vehicle['model']} {vehicle['year']} - R${vehicle['price']:.2f}")
        
        vehicle_id = self.get_input("ID do veículo", int)
        vehicle = self.db.get_vehicle_by_id(vehicle_id)
        
        if not vehicle or vehicle['status'] != 'Available':
            print("Veículo não disponível!")
            self.wait_for_enter()
            return
        
        # Show customers
        customers = self.db.get_customers()
        if not customers:
            print("Nenhum cliente cadastrado!")
            self.wait_for_enter()
            return
        
        print("\nClientes:")
        for customer in customers:
            print(f"ID {customer['id']}: {customer['name']} - {customer['email']}")
        
        customer_id = self.get_input("ID do cliente", int)
        customer = self.db.get_customer_by_id(customer_id)
        
        if not customer:
            print("Cliente não encontrado!")
            self.wait_for_enter()
            return
        
        sale_price = self.get_input(f"Preço de venda (sugerido: R${vehicle['price']:.2f})", float)
        payment_method = self.get_input("Método de pagamento", str, False) or "Cash"
        notes = self.get_input("Observações", str, False) or ""
        
        try:
            sale_id = self.db.add_sale(customer_id, vehicle_id, sale_price, payment_method, notes)
            print(f"Venda registrada com sucesso! ID: {sale_id}")
        except Exception as e:
            print(f"Erro ao registrar venda: {e}")
        
        self.wait_for_enter()
    
    def list_sales(self):
        """List all sales"""
        self.clear_screen()
        self.print_header("LISTA DE VENDAS")
        
        sales = self.db.get_sales()
        
        if not sales:
            print("Nenhuma venda encontrada.")
        else:
            for sale in sales:
                print(f"Venda ID: {sale['id']}")
                print(f"Cliente: {sale['customer_name']} ({sale['customer_email']})")
                print(f"Veículo: {sale['brand']} {sale['model']} {sale['year']} - {sale['color']}")
                print(f"Preço: R${sale['sale_price']:.2f}")
                print(f"Data: {sale['sale_date']}")
                print(f"Pagamento: {sale['payment_method']}")
                if sale['notes']:
                    print(f"Observações: {sale['notes']}")
                print("-" * 50)
        
        self.wait_for_enter()
    
    def employee_menu(self):
        """Employee management menu"""
        while True:
            options = [
                "Adicionar Funcionário",
                "Listar Funcionários"
            ]
            
            self.print_menu("GERENCIAR FUNCIONÁRIOS", options)
            choice = self.get_input("Escolha uma opção", int, False)
            
            if choice == 1:
                self.add_employee()
            elif choice == 2:
                self.list_employees()
            elif choice == 0:
                break
            else:
                print("Opção inválida!")
                self.wait_for_enter()
    
    def add_employee(self):
        """Add a new employee"""
        self.clear_screen()
        self.print_header("ADICIONAR FUNCIONÁRIO")
        
        name = self.get_input("Nome")
        email = self.get_input("Email")
        position = self.get_input("Cargo")
        salary_str = self.get_input("Salário", str, False)
        salary = float(salary_str) if salary_str else 0.0
        
        try:
            employee_id = self.db.add_employee(name, email, position, salary)
            print(f"Funcionário adicionado com sucesso! ID: {employee_id}")
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
        
        self.wait_for_enter()
    
    def list_employees(self):
        """List all employees"""
        self.clear_screen()
        self.print_header("LISTA DE FUNCIONÁRIOS")
        
        employees = self.db.get_employees()
        
        if not employees:
            print("Nenhum funcionário encontrado.")
        else:
            print(f"{'ID':<5} {'Nome':<20} {'Email':<25} {'Cargo':<15} {'Salário':<10}")
            print("-" * 80)
            for employee in employees:
                salary_str = f"R${employee['salary']:.2f}" if employee['salary'] else "N/A"
                print(f"{employee['id']:<5} {employee['name']:<20} {employee['email']:<25} "
                      f"{employee['position']:<15} {salary_str:<10}")
        
        self.wait_for_enter()
    
    def reports_menu(self):
        """Reports menu"""
        self.clear_screen()
        self.print_header("RELATÓRIOS")
        
        summary = self.db.get_sales_summary()
        
        print(f"Total de Vendas: {summary.get('total_sales', 0)}")
        print(f"Receita Total: R${summary.get('total_revenue', 0):.2f}")
        print(f"Veículos Disponíveis: {summary.get('available_vehicles', 0)}")
        print(f"Total de Clientes: {summary.get('total_customers', 0)}")
        
        self.wait_for_enter()
    
    def search_vehicles(self):
        """Search vehicles"""
        self.clear_screen()
        self.print_header("BUSCAR VEÍCULOS")
        
        query = self.get_input("Digite marca, modelo ou cor")
        vehicles = self.db.search_vehicles(query)
        
        if not vehicles:
            print("Nenhum veículo encontrado.")
        else:
            print(f"{'ID':<5} {'Marca':<12} {'Modelo':<15} {'Ano':<6} {'Cor':<10} {'Preço':<12} {'Status':<10}")
            print("-" * 80)
            for vehicle in vehicles:
                print(f"{vehicle['id']:<5} {vehicle['brand']:<12} {vehicle['model']:<15} "
                      f"{vehicle['year']:<6} {vehicle['color']:<10} R${vehicle['price']:<11.2f} {vehicle['status']:<10}")
        
        self.wait_for_enter()

if __name__ == "__main__":
    app = TerminalInterface()
    app.run()
