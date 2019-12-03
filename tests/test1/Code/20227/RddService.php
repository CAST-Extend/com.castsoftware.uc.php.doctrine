<?php
namespace AppBundle\Service;

use Doctrine\ORM\EntityManager;
use AppBundle\Entity\Utilisateur;
use AppBundle\Entity\TypeDiligence;

class RddService
{
	private $em;

	private $logBaseDir = "/rdd_log/";
	private $dirName;
	private $fileName;
	private $showDetail;
	private $projectDir;
	private $dirCsv;
	private $dirXml;
	private $dirSql;
	private $dirLog;

	private $initProfil = array(
		'id' => 1,
		'libelle' => "REDACTEUR_XXXR",
		'role' => "REDACTEUR_XXXR"
	);

	private $forbidden = array("A","TEST");

	private $initEtat = array(
		array(
			'id' => 1,
			'libelle' => "En cours"
		),
		array(
			'id' => 2,
			'libelle' => "Classée"
		)
	);

	private $initParametre = array(
		array(
			'id' => 1,
			'id_utilisateur' => 1,
			'type_parametre' => "xxx",
			'json_data' => '{"accueil":{"xxx":2,"type_delai":1},"xxx":{"xxx":1,"xxx":1,"xxx":2,"xxx":2}}',
			'date_creation' => "current_timestamp",
			'date_modification' => "null"
		),
		array(
			'id' => 2,
			'id_utilisateur' => 1,
			'type_parametre' => "xxx",
			'json_data' => '{"xxx":1}',
			'date_creation' => "current_timestamp",
			'date_modification' => "null"
		)	
	);

	private $initDegre = array(
		array(
			'id' => 1,
			'libelle' => "xxx xxx"
		),
		array(
			'id' => 2,
			'libelle' => "xxx xxx"
		),
		array(
			'id' => 3,
			'libelle' => "xxx xxx"
		)
	);

	private $initPositionChancelier = array(
		array(
			'id' => 1,
			'libelle' => "xxx"
		),
		array(
			'id' => 2,
			'libelle' => "xxx"
		),
		array(
			'id' => 3,
			'libelle' => "xxx xxx"
		),
		array(
			'id' => 4,
			'libelle' => "xxx"
		),
		array(
			'id' => 5,
			'libelle' => "xxx à xx"
		)
	);

	private $initTypeAffaire = array(
		array(
			'id' => 1,
			'libelle' => "xxx",
			'identification' => "X",
			'code' => "CX",
			'datefin' => "2019-01-01",
			'date_creation' => "current_timestamp",
			'date_modification' => "null",
			'date_suppression' => "null"
		),
		array(
			'id' => 2,
			'libelle' => "xxx",
			'identification' => "S",
			'code' => "CS",
			'datefin' => "null",
			'date_creation' => "current_timestamp",
			'date_modification' => "null",
			'date_suppression' => "null"
		),
		array(
			'id' => 3,
			'libelle' => "xxx",
			'identification' => "C",
			'code' => "CN",
			'datefin' => "null",
			'date_creation' => "current_timestamp",
			'date_modification' => "null",
			'date_suppression' => "null"
		),
		array(
			'id' => 4,
			'libelle' => "déclaration",
			'identification' => "D",
			'code' => "DN",
			'datefin' => "null",
			'date_creation' => "current_timestamp",
			'date_modification' => "null",
			'date_suppression' => "null"
		),
		array(
			'id' => 5,
			'libelle' => "xxx xxx",
			'identification' => "C",
			'code' => "RG",
			'datefin' => "null",
			'date_creation' => "current_timestamp",
			'date_modification' => "null",
			'date_suppression' => "null"
		),
		array(
			'id' => 6,
			'libelle' => "déclaration ti",
			'identification' => "D",
			'code' => "DT",
			'datefin' => "null",
			'date_creation' => "current_timestamp",
			'date_modification' => "null",
			'date_suppression' => "null"
		)
	);

	public function __construct(EntityManager $entityManager, $projectDir, $dirCsv, $dirXml, $dirSql, $dirLog)
	{
		$this->em = $entityManager;
		$this->projectDir = $projectDir;
		$this->dirName = date("Y-m-d");
		$this->fileName = "log-" . date("Y-m-d-H-i-s");
		$this->dirCsv = $dirCsv;
		$this->dirXml = $dirXml;
		$this->dirSql = $dirSql;
		$this->dirLog = $dirLog;
	}

	public function generateSQL($table, $showDetail, $truncate)
	{
		$this->showDetail = $showDetail;

		switch ($table)
		{
			case 'xxx':
			case 'xxx':
			case 'xxx':
			case 'xxx':
			case 'xxx':
				$typeFile = 'xml';
				break;
			case 'all':
				$this->generateAllSql();
				break;
			default:
				$typeFile = 'csv';
				break;
		}

		if($table != "all")
		{
			$this->traitement($table, $typeFile, $truncate, $this->showDetail);
		}
	}

	private function generateAllSql()
	{
		$start = microtime(true);
		$truncate = false;
		$showDetail = $this->showDetail;

		$this->traitement('init', '', $truncate, $showDetail);

		$this->traitement('xxx', 'csv', $truncate, $showDetail);
		$this->echo_seprater();		

		$this->traitement('xxx', 'csv', $truncate, $showDetail);
		$this->echo_seprater();

		$this->traitement('xxx', 'csv', $truncate, $showDetail);
		$this->echo_seprater();


		$this->traitement('xxx', 'csv', $truncate, $showDetail);
		$this->echo_seprater();

		$this->traitement('xxx', 'csv', $truncate, $showDetail);
		$this->echo_seprater();

		$this->traitement('xxx', '', $truncate, $showDetail);

		$seconds = microtime(true) - $start;
		$hours = floor($seconds / 3600);
		$minutes = floor(($seconds / 60) % 60);
		$seconds = $seconds % 60;

		echo "All done in " . $hours . "h" . $minutes . "m" . $seconds . "s\n\r";
	}

	private function traitement($table, $typeFile="csv", $truncate = true, $showDetail = true)
	{
		$onlyLog = true;

		if($typeFile == 'csv'){
			$pathFile = $this->dirCsv."/";
		}else{
			$pathFile = $this->dirXml."/";
		}
		$file = "";

		switch ($table){
			case "parents":
			case "xxx":
			case "xxx":		$file = "xxx.CSV";
			break;
			case "xxx":			$file = "xxx.xml";
			break;
			case "xxx":		$file = "xxx.CSV";
			break;
			case "xxx":	$file = "xxx.CSV";
			break;
		}

		if($file != "")
		{
			$pathFile = $pathFile.$file;

			if($typeFile == 'csv')
			{
				$arrFromCSV = $this->csv_to_array($pathFile,$table);
			}
			else
			{
				$xml=simplexml_load_file($pathFile) or die("Error: Cannot create object");
			}

			if($table == "xxx" || $table == "tome")
			{
				$dataDossier = [];
				$dataTome = [];
				foreach ($arrFromCSV as $key => $value) 
				{
					$arrFromCSV[$key]['dos_num'] = $dos_num = str_replace(' ', '', $value['dos_num']);
					/*$xxx = "2019Y205C500";*/
					$pattern1 = '/^\d+Y/';
					$numeros = preg_split($pattern1, $dos_num);
					$pattern2 = '/[a-zA-Z]\d+$/';
					preg_match($pattern2, $numeros[1], $matches);
					
					if($table == "xxx" && count($matches) === 0)
					{
						$dataDossier[] = $arrFromCSV[$key];
					}
					else if($table == "tome" && count($matches) > 0)
					{
						$numTome = $matches[0];
						$numDossier = rtrim($dos_num, $numTome);
						$arrFromCSV[$key]['xxx'] = $numDossier;
						$arrFromCSV[$key]['xxx'] = $numTome;
						$dataTome[] = $arrFromCSV[$key];
					}
				}
			}
		}
		

	}
}
