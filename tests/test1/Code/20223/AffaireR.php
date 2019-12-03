<?php
namespace NatachaBundle\Entity;

use DateTime;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints\Date;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Routing\Annotation\Route;
use JMS\Serializer\Annotation as JMS;

/**
 * AffaireR
 * @ORM\Table(name="affaire_r")
 * @ORM\Entity(repositoryClass="NatachaBundle\Repository\AffaireRRepository")
 * @ORM\Entity
 * @ORM\Table(name="affaire_r")
 */
class AffaireR extends Affaire
{
    /**
     * @var int
     * @ORM\Column(type="bigint")
     * @ORM\Id
     * @ORM\GeneratedValue(strategy="AUTO")
     * @JMS\Groups({"getDossier"})
     */
    protected $id;

    /**
     * @var DateTime
     * @ORM\Column(name="date_reception", type="date", nullable=true)
     */
    private $dateReception;

    /**
     * @var DateTime
     * @ORM\Column(name="date_fermeture", type="date", nullable=true)
     */
    private $dateFermeture;

   

    /**
     * @var bool
     * @ORM\Column(name="is_archivable", type="boolean", options={"default":"0"})
     */
    private $isArchivable;


    /**
     * @return int
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * @param int $id
     * @return AffaireR
     */
    public function setId($id)
    {
        $this->id = $id;
        return $this;
    }

    /**
     * @return DateTime
     */
    public function getDateReception()
    {
        return $this->dateOuverture;
    }

    /**
     * @param DateTime $dateReception
     * @return AffaireR
     */
    public function setDateReception($dateReception)
    {
        $this->dateReception = $dateReception;
        return $this;
    }

    /**
     * @return DateTime
     */
    public function getDateFermeture()
    {
        return $this->dateFermeture;
    }

    /**
     * @param DateTime $dateFermeture
     * @return AffaireR
     */
    public function setDateFermeture($dateFermeture)
    {
        $this->dateFermeture = $dateFermeture;
        return $this;
    }

    /**
     * Set isArchivable
     * @param boolean $isArchivable
     */
    public function setIsArchivable(bool $isArchivable)
    {
        $this->isArchivable = $isArchivable;
        return $this;
    }

    /**
     * Get isArchivable
     * @return boolean
     */
    public function getIsArchivable()
    {
        return $this->isArchivable;
    }


}
