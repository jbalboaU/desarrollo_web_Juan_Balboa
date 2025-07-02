package Project.Spring_project.models;

import jakarta.persistence.*;
import Project.Spring_project.models.Nota;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

@Entity
@Table(name = "nota", schema="tarea2")
public class Nota {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "valor")
    @Min(1)
    @Max(7)
    private int valor;

    @ManyToOne
    @JoinColumn(name="actividad_id", nullable=false)
    private Actividad actividad;

    public Nota(){
    }

    public Nota(int valor){
        this.valor=valor;
    }

    public Long getId(){
        return id;
    }

    public int getValor(){
        return valor;
    }

    public Actividad getActividad(){
        return actividad;
    }

    public void setActividad(Actividad actividad){
        this.actividad=actividad;
    }

    public void setValor(int valor){
        this.valor=valor;
    }
}
