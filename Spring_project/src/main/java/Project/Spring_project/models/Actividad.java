package Project.Spring_project.models;


import java.time.LocalDateTime;

import jakarta.persistence.*;
import java.util.List;

import org.springframework.format.annotation.DateTimeFormat;

import jakarta.validation.constraints.NotNull;

@Entity
@Table(name="actividad", schema="tarea2")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    
    @NotNull
    @DateTimeFormat(pattern = "yyyy-MM-dd'T'HH:mm")
    @Column(name="dia_hora_inicio", nullable=false)
    private LocalDateTime fechaInicio;

    @Column(name = "dia_hora_termino")
    private LocalDateTime fechaTermino;

    private String sector;

    @NotNull
    private String nombre;

    @OneToMany(mappedBy = "actividad", fetch=FetchType.LAZY)
    private List<Actividad_Tema> temas;

    @OneToMany(mappedBy = "actividad")
    private List<Nota> notas;

    public Actividad(){
    }

    public Actividad(LocalDateTime fechaInicio,
                    LocalDateTime fechaTermino,
                    String sector,
                    String nombre,
                    List<Actividad_Tema> temas,
                    List<Nota> notas
                    ){
        this.fechaInicio = fechaInicio;
        this.fechaTermino=fechaTermino;
        this.sector=sector;
        this.nombre=nombre;
        this.temas=temas;
        this.notas=notas;
    }
    public int getId(){
        return id;
    }
    
    public LocalDateTime getFechaInicio(){
        return fechaInicio;
    }

    public LocalDateTime getFechaTermino(){
        return fechaTermino;
    }

    public String getSector(){
        return sector;
    }

    public String getNombre(){
        return nombre;
    }

    public List<Actividad_Tema> getTemas(){
        return temas;
    }
    public List<Nota> getNotas(){
        return notas;
    }
}


