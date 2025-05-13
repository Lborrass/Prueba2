from datetime import datetime, date
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Proyecto:
    ESTADOS_VALIDOS = {"En curso", "Finalizado", "Cancelado"}

    def __init__(self, id_usuario, codigo_proyecto, fecha_inicio, fecha_estimacion_terminacion,
                 horas_jefe, horas_proyectista, costo_subcontratacion, gastos, ingreso,
                 tarifa_hora_jefe, tarifa_hora_proyectista, estado="En curso",
                 fecha_efectiva_terminacion=None):

        self.id_usuario = id_usuario
        self.codigo_proyecto = codigo_proyecto
        self.fecha_inicio = fecha_inicio
        self.fecha_estimacion_terminacion = fecha_estimacion_terminacion
        self.fecha_efectiva_terminacion = fecha_efectiva_terminacion
        self.horas_jefe = horas_jefe
        self.horas_proyectista = horas_proyectista
        self.costo_subcontratacion = costo_subcontratacion
        self.gastos = gastos
        self.ingreso = ingreso
        self.tarifa_hora_jefe = tarifa_hora_jefe
        self.tarifa_hora_proyectista = tarifa_hora_proyectista

        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Debe ser uno de {self.ESTADOS_VALIDOS}")
        self.estado = estado

        self.validar_fechas()

    def calcular_costo_total(self):
        return (self.horas_jefe * self.tarifa_hora_jefe) + \
               (self.horas_proyectista * self.tarifa_hora_proyectista) + \
               self.costo_subcontratacion + self.gastos

    def calcular_rentabilidad(self):
        costo_total = self.calcular_costo_total()
        return ((self.ingreso - costo_total) / costo_total) * 100 if costo_total else 0

    def registrar_fecha_efectiva_terminacion(self, fecha_efectiva):
        if fecha_efectiva < self.fecha_inicio:
            raise ValueError("La fecha efectiva no puede ser anterior a la fecha de inicio.")
        self.fecha_efectiva_terminacion = fecha_efectiva
        self.estado = "Finalizado"

    def cancelar_proyecto(self):
        self.estado = "Cancelado"
        self.fecha_efectiva_terminacion = date.today()

    def evaluar_estimacion(self):
        if self.estado != "Finalizado" or not self.fecha_efectiva_terminacion:
            return "Proyecto en curso"
        return "Adecuada" if self.fecha_efectiva_terminacion <= self.fecha_estimacion_terminacion else "Inadecuada"

    def validar_fechas(self):
        if self.fecha_inicio > self.fecha_estimacion_terminacion:
            raise ValueError("La fecha de inicio no puede ser posterior a la estimada de terminación.")
        if self.fecha_efectiva_terminacion and self.fecha_inicio > self.fecha_efectiva_terminacion:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha efectiva de terminación.")

    def resumen_proyecto(self):
        return {
            "Código Proyecto": self.codigo_proyecto,
            "Usuario Responsable": self.id_usuario,
            "Estado": self.estado,
            "Fechas": {
                "Inicio": self.fecha_inicio,
                "Estimada Terminación": self.fecha_estimacion_terminacion,
                "Efectiva Terminación": self.fecha_efectiva_terminacion
            },
            "Costos": {
                "Total": self.calcular_costo_total(),
                "Ingreso": self.ingreso
            },
            "Rentabilidad (%)": round(self.calcular_rentabilidad(), 2),
            "Evaluación Estimación": self.evaluar_estimacion()
        }

def main():
    proyectos = []

    def registrar_proyecto():
        try:
            fecha_inicio = datetime.strptime(entry_fecha_inicio.get(), "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(entry_fecha_fin.get(), "%Y-%m-%d").date()
            proyecto = Proyecto(
                id_usuario=entry_usuario.get(),
                codigo_proyecto=entry_codigo.get(),
                fecha_inicio=fecha_inicio,
                fecha_estimacion_terminacion=fecha_fin,
                horas_jefe=float(entry_horas_jefe.get()),
                horas_proyectista=float(entry_horas_proyectista.get()),
                costo_subcontratacion=float(entry_subcontratacion.get()),
                gastos=float(entry_gastos.get()),
                ingreso=float(entry_ingreso.get()),
                tarifa_hora_jefe=float(entry_tarifa_jefe.get()),
                tarifa_hora_proyectista=float(entry_tarifa_proyectista.get())
            )
            proyectos.append(proyecto)
            messagebox.showinfo("Éxito", "Proyecto registrado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    root = tk.Tk()
    root.title("Registro de Proyecto - Ashes Fire")
    root.geometry("500x700")

    logo_img = Image.open("ashes_fire_logo.png")
    logo_img = logo_img.resize((300, 80), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    panel = tk.Label(root, image=logo)
    panel.pack(pady=10)

    tk.Label(root, text="Formulario de Registro de Proyecto", font=("Arial", 14, "bold")).pack(pady=5)
    frame = tk.Frame(root)
    frame.pack(pady=10)

    campos = [
        ("ID Usuario", "entry_usuario"),
        ("Código Proyecto", "entry_codigo"),
        ("Fecha Inicio (YYYY-MM-DD)", "entry_fecha_inicio"),
        ("Fecha Estimada Fin (YYYY-MM-DD)", "entry_fecha_fin"),
        ("Horas Jefe Proyecto", "entry_horas_jefe"),
        ("Horas Proyectista", "entry_horas_proyectista"),
        ("Costo Subcontratación", "entry_subcontratacion"),
        ("Gastos", "entry_gastos"),
        ("Ingreso Proyecto", "entry_ingreso"),
        ("Tarifa Hora Jefe", "entry_tarifa_jefe"),
        ("Tarifa Hora Proyectista", "entry_tarifa_proyectista"),
    ]

    entries = {}
    for label_text, var_name in campos:
        tk.Label(frame, text=label_text).pack()
        entry = tk.Entry(frame)
        entry.pack()
        entries[var_name] = entry

    globals().update(entries)

    tk.Button(root, text="Registrar Proyecto", command=registrar_proyecto, bg="red", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
