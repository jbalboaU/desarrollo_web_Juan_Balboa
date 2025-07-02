package Project.Spring_project.models;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RepositorioNota extends JpaRepository<Nota, Long>{
    List<Nota> findByActividad(Actividad actividad);
}
