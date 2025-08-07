import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import DatabaseManager
import threading

class GUIInterface:
    def __init__(self):
        self.db = DatabaseManager()
        self.root = tk.Tk()
        self.root.title("Sistema de Concessionária")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Left sidebar with buttons
        sidebar = ttk.Frame(main_frame, padding="5")
        sidebar.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Title
        title_label = ttk.Label(sidebar, text="Sistema de\nConcessionária", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Menu buttons
        buttons = [
            ("Veículos", self.show_vehicles),
            ("Clientes", self.show_customers),
            ("Vendas", self.show_sales),
            ("Funcionários", self.show_employees),
            ("Relatórios", self.show_reports),
            ("Buscar", self.show_search)
        ]
        
        for i, (text, command) in enumerate(buttons, 1):
            btn = ttk.Button(sidebar, text=text, command=command, width=15)
            btn.grid(row=i, column=0, pady=2, sticky=(tk.W, tk.E))
        
        # Main content area
        self.content_frame = ttk.Frame(main_frame, padding="5")
        self.content_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        
        # Show vehicles by default
        self.show_vehicles()
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_vehicles(self):
        """Show vehicles management interface"""
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Gerenciar Veículos", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(btn_frame, text="Adicionar Veículo", 
                  command=self.add_vehicle_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Atualizar", 
                  command=self.refresh_vehicles).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Editar Selecionado", 
                  command=self.edit_vehicle_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remover Selecionado", 
                  command=self.delete_vehicle_dialog).pack(side=tk.LEFT)
        
        # Treeview for vehicles
        columns = ('ID', 'Marca', 'Modelo', 'Ano', 'Cor', 'Preço', 'Status')
        self.vehicles_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        
        for col in columns:
            self.vehicles_tree.heading(col, text=col)
            self.vehicles_tree.column(col, width=100)
        
        self.vehicles_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, 
                                 command=self.vehicles_tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.vehicles_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_vehicles()
    
    def refresh_vehicles(self):
        """Refresh vehicles list"""
        # Clear existing items
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)
        
        # Load vehicles
        vehicles = self.db.get_vehicles()
        for vehicle in vehicles:
            self.vehicles_tree.insert('', tk.END, values=(
                vehicle['id'], vehicle['brand'], vehicle['model'], 
                vehicle['year'], vehicle['color'], f"R${vehicle['price']:.2f}", 
                vehicle['status']
            ))
    
    def add_vehicle_dialog(self):
        """Show add vehicle dialog"""
        dialog = VehicleDialog(self.root, "Adicionar Veículo")
        if dialog.result:
            try:
                self.db.add_vehicle(**dialog.result)
                messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso!")
                self.refresh_vehicles()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar veículo: {e}")
    
    def edit_vehicle_dialog(self):
        """Show edit vehicle dialog"""
        selection = self.vehicles_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um veículo para editar.")
            return
        
        item = self.vehicles_tree.item(selection[0])
        vehicle_id = item['values'][0]
        vehicle = self.db.get_vehicle_by_id(vehicle_id)
        
        if not vehicle:
            messagebox.showerror("Erro", "Veículo não encontrado!")
            return
        
        dialog = VehicleDialog(self.root, "Editar Veículo", vehicle)
        if dialog.result:
            try:
                self.db.update_vehicle(vehicle_id, **dialog.result)
                messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso!")
                self.refresh_vehicles()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar veículo: {e}")
    
    def delete_vehicle_dialog(self):
        """Delete selected vehicle"""
        selection = self.vehicles_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um veículo para remover.")
            return
        
        item = self.vehicles_tree.item(selection[0])
        vehicle_id = item['values'][0]
        vehicle_info = f"{item['values'][1]} {item['values'][2]} {item['values'][3]}"
        
        if messagebox.askyesno("Confirmar", f"Remover veículo {vehicle_info}?"):
            try:
                self.db.delete_vehicle(vehicle_id)
                messagebox.showinfo("Sucesso", "Veículo removido com sucesso!")
                self.refresh_vehicles()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover veículo: {e}")
    
    def show_customers(self):
        """Show customers management interface"""
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Gerenciar Clientes", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(btn_frame, text="Adicionar Cliente", 
                  command=self.add_customer_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Atualizar", 
                  command=self.refresh_customers).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Editar Selecionado", 
                  command=self.edit_customer_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remover Selecionado", 
                  command=self.delete_customer_dialog).pack(side=tk.LEFT)
        
        # Treeview for customers
        columns = ('ID', 'Nome', 'Email', 'Telefone', 'CPF')
        self.customers_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=150)
        
        self.customers_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, 
                                 command=self.customers_tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.customers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_customers()
    
    def refresh_customers(self):
        """Refresh customers list"""
        # Clear existing items
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        # Load customers
        customers = self.db.get_customers()
        for customer in customers:
            self.customers_tree.insert('', tk.END, values=(
                customer['id'], customer['name'], customer['email'], 
                customer['phone'], customer.get('cpf', '')
            ))
    
    def add_customer_dialog(self):
        """Show add customer dialog"""
        dialog = CustomerDialog(self.root, "Adicionar Cliente")
        if dialog.result:
            try:
                self.db.add_customer(**dialog.result)
                messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
                self.refresh_customers()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar cliente: {e}")
    
    def edit_customer_dialog(self):
        """Show edit customer dialog"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return
        
        item = self.customers_tree.item(selection[0])
        customer_id = item['values'][0]
        customer = self.db.get_customer_by_id(customer_id)
        
        if not customer:
            messagebox.showerror("Erro", "Cliente não encontrado!")
            return
        
        dialog = CustomerDialog(self.root, "Editar Cliente", customer)
        if dialog.result:
            try:
                self.db.update_customer(customer_id, **dialog.result)
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                self.refresh_customers()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")
    
    def delete_customer_dialog(self):
        """Delete selected customer"""
        selection = self.customers_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para remover.")
            return
        
        item = self.customers_tree.item(selection[0])
        customer_id = item['values'][0]
        customer_name = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Remover cliente {customer_name}?"):
            try:
                self.db.delete_customer(customer_id)
                messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
                self.refresh_customers()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover cliente: {e}")
    
    def show_sales(self):
        """Show sales management interface"""
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Gerenciar Vendas", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(btn_frame, text="Registrar Venda", 
                  command=self.add_sale_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Atualizar", 
                  command=self.refresh_sales).pack(side=tk.LEFT)
        
        # Treeview for sales
        columns = ('ID', 'Cliente', 'Veículo', 'Preço', 'Data', 'Pagamento')
        self.sales_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=150)
        
        self.sales_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, 
                                 command=self.sales_tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_sales()
    
    def refresh_sales(self):
        """Refresh sales list"""
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Load sales
        sales = self.db.get_sales()
        for sale in sales:
            vehicle_info = f"{sale['brand']} {sale['model']} {sale['year']}"
            self.sales_tree.insert('', tk.END, values=(
                sale['id'], sale['customer_name'], vehicle_info,
                f"R${sale['sale_price']:.2f}", sale['sale_date'][:10], 
                sale['payment_method']
            ))
    
    def add_sale_dialog(self):
        """Show add sale dialog"""
        dialog = SaleDialog(self.root, self.db)
        if dialog.result:
            try:
                self.db.add_sale(**dialog.result)
                messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
                self.refresh_sales()
                # Refresh vehicles if showing vehicles
                if hasattr(self, 'vehicles_tree'):
                    self.refresh_vehicles()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao registrar venda: {e}")
    
    def show_employees(self):
        """Show employees management interface"""
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Gerenciar Funcionários", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Buttons frame
        btn_frame = ttk.Frame(self.content_frame)
        btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(btn_frame, text="Adicionar Funcionário", 
                  command=self.add_employee_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Atualizar", 
                  command=self.refresh_employees).pack(side=tk.LEFT)
        
        # Treeview for employees
        columns = ('ID', 'Nome', 'Email', 'Cargo', 'Salário')
        self.employees_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        
        for col in columns:
            self.employees_tree.heading(col, text=col)
            self.employees_tree.column(col, width=150)
        
        self.employees_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, 
                                 command=self.employees_tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.employees_tree.configure(yscrollcommand=scrollbar.set)
        
        self.refresh_employees()
    
    def refresh_employees(self):
        """Refresh employees list"""
        # Clear existing items
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        # Load employees
        employees = self.db.get_employees()
        for employee in employees:
            salary_str = f"R${employee['salary']:.2f}" if employee['salary'] else "N/A"
            self.employees_tree.insert('', tk.END, values=(
                employee['id'], employee['name'], employee['email'], 
                employee['position'], salary_str
            ))
    
    def add_employee_dialog(self):
        """Show add employee dialog"""
        dialog = EmployeeDialog(self.root, "Adicionar Funcionário")
        if dialog.result:
            try:
                self.db.add_employee(**dialog.result)
                messagebox.showinfo("Sucesso", "Funcionário adicionado com sucesso!")
                self.refresh_employees()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao adicionar funcionário: {e}")
    
    def show_reports(self):
        """Show reports interface"""
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Relatórios", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Get summary data
        summary = self.db.get_sales_summary()
        
        # Create report frame
        report_frame = ttk.LabelFrame(self.content_frame, text="Resumo Geral", padding="10")
        report_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Report data
        reports = [
            ("Total de Vendas:", summary.get('total_sales', 0)),
            ("Receita Total:", f"R${summary.get('total_revenue', 0):.2f}"),
            ("Veículos Disponíveis:", summary.get('available_vehicles', 0)),
            ("Total de Clientes:", summary.get('total_customers', 0))
        ]
        
        for i, (label, value) in enumerate(reports):
            ttk.Label(report_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=2)
            ttk.Label(report_frame, text=str(value), font=('Arial', 10)).grid(
                row=i, column=1, sticky=tk.W, padx=(20, 0), pady=2)
    
    def show_search(self):
        """Show search interface"""
        self.clear_content()
        
        # Title
        title = ttk.Label(self.content_frame, text="Buscar Veículos", 
                         font=('Arial', 14, 'bold'))
        title.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Search frame
        search_frame = ttk.Frame(self.content_frame)
        search_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar por marca, modelo ou cor:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Button(search_frame, text="Buscar", command=self.perform_search).pack(side=tk.LEFT)
        
        # Results treeview
        columns = ('ID', 'Marca', 'Modelo', 'Ano', 'Cor', 'Preço', 'Status')
        self.search_tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=100)
        
        self.search_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, 
                                 command=self.search_tree.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        # Bind Enter key to search
        search_entry.bind('<Return>', lambda e: self.perform_search())
    
    def perform_search(self):
        """Perform vehicle search"""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Aviso", "Digite um termo para buscar.")
            return
        
        # Clear existing items
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        # Search vehicles
        vehicles = self.db.search_vehicles(query)
        for vehicle in vehicles:
            self.search_tree.insert('', tk.END, values=(
                vehicle['id'], vehicle['brand'], vehicle['model'], 
                vehicle['year'], vehicle['color'], f"R${vehicle['price']:.2f}", 
                vehicle['status']
            ))
        
        if not vehicles:
            messagebox.showinfo("Resultado", "Nenhum veículo encontrado.")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

class VehicleDialog:
    def __init__(self, parent, title, vehicle=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Marca:", "brand"),
            ("Modelo:", "model"),
            ("Ano:", "year"),
            ("Cor:", "color"),
            ("Preço:", "price"),
            ("Quilometragem:", "mileage"),
            ("Combustível:", "fuel_type"),
            ("Transmissão:", "transmission")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            self.entries[field] = entry
        
        # Special handling for fuel_type and transmission dropdowns
        fuel_values = ["Gasoline", "Flex", "Diesel", "Electric", "Hybrid"]
        transmission_values = ["Manual", "Automatic", "CVT"]
        
        # Replace fuel_type entry with combobox
        self.entries['fuel_type'].destroy()
        fuel_combo = ttk.Combobox(main_frame, values=fuel_values, width=27, state="readonly")
        fuel_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        fuel_combo.set("Gasoline")
        self.entries['fuel_type'] = fuel_combo
        
        # Replace transmission entry with combobox
        self.entries['transmission'].destroy()
        trans_combo = ttk.Combobox(main_frame, values=transmission_values, width=27, state="readonly")
        trans_combo.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        trans_combo.set("Manual")
        self.entries['transmission'] = trans_combo
        
        # Pre-fill if editing
        if vehicle:
            self.entries['brand'].insert(0, vehicle.get('brand', ''))
            self.entries['model'].insert(0, vehicle.get('model', ''))
            self.entries['year'].insert(0, str(vehicle.get('year', '')))
            self.entries['color'].insert(0, vehicle.get('color', ''))
            self.entries['price'].insert(0, str(vehicle.get('price', '')))
            self.entries['mileage'].insert(0, str(vehicle.get('mileage', 0)))
            self.entries['fuel_type'].set(vehicle.get('fuel_type', 'Gasoline'))
            self.entries['transmission'].set(vehicle.get('transmission', 'Manual'))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Salvar", command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Focus on first entry
        self.entries['brand'].focus()
    
    def save(self):
        """Save the vehicle data"""
        try:
            data = {
                'brand': self.entries['brand'].get().strip(),
                'model': self.entries['model'].get().strip(),
                'year': int(self.entries['year'].get()),
                'color': self.entries['color'].get().strip(),
                'price': float(self.entries['price'].get()),
                'mileage': int(self.entries['mileage'].get() or 0),
                'fuel_type': self.entries['fuel_type'].get(),
                'transmission': self.entries['transmission'].get()
            }
            
            # Validate required fields
            if not all([data['brand'], data['model'], data['color']]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
            
            if data['year'] < 1900 or data['year'] > 2030:
                messagebox.showerror("Erro", "Ano deve estar entre 1900 e 2030!")
                return
            
            if data['price'] <= 0:
                messagebox.showerror("Erro", "Preço deve ser maior que zero!")
                return
            
            self.result = data
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Verifique os valores numéricos!")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()

class CustomerDialog:
    def __init__(self, parent, title, customer=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Nome:", "name"),
            ("Email:", "email"),
            ("Telefone:", "phone"),
            ("Endereço:", "address"),
            ("CPF:", "cpf")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            self.entries[field] = entry
        
        # Pre-fill if editing
        if customer:
            self.entries['name'].insert(0, customer.get('name', ''))
            self.entries['email'].insert(0, customer.get('email', ''))
            self.entries['phone'].insert(0, customer.get('phone', ''))
            self.entries['address'].insert(0, customer.get('address', ''))
            self.entries['cpf'].insert(0, customer.get('cpf', ''))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Salvar", command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Focus on first entry
        self.entries['name'].focus()
    
    def save(self):
        """Save the customer data"""
        try:
            data = {
                'name': self.entries['name'].get().strip(),
                'email': self.entries['email'].get().strip(),
                'phone': self.entries['phone'].get().strip(),
                'address': self.entries['address'].get().strip(),
                'cpf': self.entries['cpf'].get().strip()
            }
            
            # Validate required fields
            if not all([data['name'], data['email'], data['phone']]):
                messagebox.showerror("Erro", "Preencha nome, email e telefone!")
                return
            
            # Basic email validation
            if '@' not in data['email']:
                messagebox.showerror("Erro", "Email inválido!")
                return
            
            self.result = data
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()

class SaleDialog:
    def __init__(self, parent, db):
        self.result = None
        self.db = db
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Registrar Venda")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Customer selection
        ttk.Label(main_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(main_frame, textvariable=self.customer_var, 
                                          width=40, state="readonly")
        self.customer_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Vehicle selection
        ttk.Label(main_frame, text="Veículo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.vehicle_var = tk.StringVar()
        self.vehicle_combo = ttk.Combobox(main_frame, textvariable=self.vehicle_var, 
                                         width=40, state="readonly")
        self.vehicle_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Sale price
        ttk.Label(main_frame, text="Preço de Venda:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.price_entry = ttk.Entry(main_frame, width=40)
        self.price_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Payment method
        ttk.Label(main_frame, text="Método de Pagamento:").grid(row=3, column=0, sticky=tk.W, pady=5)
        payment_methods = ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Financing"]
        self.payment_combo = ttk.Combobox(main_frame, values=payment_methods, 
                                         width=37, state="readonly")
        self.payment_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.payment_combo.set("Cash")
        
        # Notes
        ttk.Label(main_frame, text="Observações:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=5)
        self.notes_text = tk.Text(main_frame, width=40, height=5)
        self.notes_text.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Load data
        self.load_customers()
        self.load_vehicles()
        
        # Bind vehicle selection to update price
        self.vehicle_combo.bind('<<ComboboxSelected>>', self.on_vehicle_selected)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Registrar Venda", command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
    
    def load_customers(self):
        """Load customers into combobox"""
        customers = self.db.get_customers()
        customer_list = [f"{c['id']} - {c['name']} ({c['email']})" for c in customers]
        self.customer_combo['values'] = customer_list
        self.customers_data = {f"{c['id']} - {c['name']} ({c['email']})": c['id'] for c in customers}
    
    def load_vehicles(self):
        """Load available vehicles into combobox"""
        vehicles = self.db.get_vehicles("Available")
        vehicle_list = [f"{v['id']} - {v['brand']} {v['model']} {v['year']} - R${v['price']:.2f}" 
                       for v in vehicles]
        self.vehicle_combo['values'] = vehicle_list
        self.vehicles_data = {f"{v['id']} - {v['brand']} {v['model']} {v['year']} - R${v['price']:.2f}": 
                             {'id': v['id'], 'price': v['price']} for v in vehicles}
    
    def on_vehicle_selected(self, event):
        """Update price when vehicle is selected"""
        selected = self.vehicle_var.get()
        if selected in self.vehicles_data:
            price = self.vehicles_data[selected]['price']
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(price))
    
    def save(self):
        """Save the sale data"""
        try:
            customer_selection = self.customer_var.get()
            vehicle_selection = self.vehicle_var.get()
            
            if not customer_selection or not vehicle_selection:
                messagebox.showerror("Erro", "Selecione cliente e veículo!")
                return
            
            customer_id = self.customers_data[customer_selection]
            vehicle_id = self.vehicles_data[vehicle_selection]['id']
            sale_price = float(self.price_entry.get())
            payment_method = self.payment_combo.get()
            notes = self.notes_text.get("1.0", tk.END).strip()
            
            if sale_price <= 0:
                messagebox.showerror("Erro", "Preço deve ser maior que zero!")
                return
            
            self.result = {
                'customer_id': customer_id,
                'vehicle_id': vehicle_id,
                'sale_price': sale_price,
                'payment_method': payment_method,
                'notes': notes
            }
            
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar venda: {e}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()

class EmployeeDialog:
    def __init__(self, parent, title, employee=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Nome:", "name"),
            ("Email:", "email"),
            ("Cargo:", "position"),
            ("Salário:", "salary")
        ]
        
        self.entries = {}
        
        for i, (label, field) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if field == "position":
                # Position dropdown
                positions = ["Manager", "Sales Representative", "Financial Analyst", 
                           "Mechanic", "Receptionist", "Marketing Specialist"]
                combo = ttk.Combobox(main_frame, values=positions, width=27, state="readonly")
                combo.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
                combo.set("Sales Representative")
                self.entries[field] = combo
            else:
                entry = ttk.Entry(main_frame, width=30)
                entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
                self.entries[field] = entry
        
        # Pre-fill if editing
        if employee:
            self.entries['name'].insert(0, employee.get('name', ''))
            self.entries['email'].insert(0, employee.get('email', ''))
            self.entries['position'].set(employee.get('position', 'Sales Representative'))
            self.entries['salary'].insert(0, str(employee.get('salary', '')))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Salvar", command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Focus on first entry
        self.entries['name'].focus()
    
    def save(self):
        """Save the employee data"""
        try:
            data = {
                'name': self.entries['name'].get().strip(),
                'email': self.entries['email'].get().strip(),
                'position': self.entries['position'].get(),
                'salary': float(self.entries['salary'].get() or 0)
            }
            
            # Validate required fields
            if not all([data['name'], data['email'], data['position']]):
                messagebox.showerror("Erro", "Preencha nome, email e cargo!")
                return
            
            # Basic email validation
            if '@' not in data['email']:
                messagebox.showerror("Erro", "Email inválido!")
                return
            
            if data['salary'] < 0:
                messagebox.showerror("Erro", "Salário não pode ser negativo!")
                return
            
            self.result = data
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Erro", "Salário inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
    
    def cancel(self):
        """Cancel the dialog"""
        self.dialog.destroy()

if __name__ == "__main__":
    app = GUIInterface()
    app.run()
