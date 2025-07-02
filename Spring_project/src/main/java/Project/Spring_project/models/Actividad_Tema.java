package Project.Spring_project.models;

import jakarta.persistence.*;

@Entity
@Table(name="actividad_tema", schema="tarea2")
public class Actividad_Tema {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Enumerated(EnumType.STRING)
    private TemaEnum tema;

    @Column(name="glosa_otro")
    private String glosaOtro;

    @ManyToOne
    @JoinColumn(name="actividad_id", nullable=false)
    private Actividad actividad;

    public enum TemaEnum{
        música, deporte, ciencias, religión, política, tecnología, juegos, baile, comida, otro
    }
    public TemaEnum getTema(){
        return tema;
    }
    
    public String getGlosaOtro(){
        return glosaOtro;
    }
    
    public void setActividad(Actividad actividad){
        this.actividad=actividad;
    }
    
}
