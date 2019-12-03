<?php

namespace NatachaBundle\Command;

use Symfony\Bundle\FrameworkBundle\Command\ContainerAwareCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputOption;


ini_set('memory_limit', '50G');
ini_set('max_execution_time', 60000);

class rddCommand extends ContainerAwareCommand
{
	protected static $defaultName = 'natacha:rdd';
	private $table = 'all';
	private $showDetail = false;
	private $truncate = true;
	private $rddService;


	protected function configure()
	{
    $this->setDescription('RDD')
         ->setHelp('This command allows you to run rdd')
         ->addOption('table', 't', InputOption::VALUE_OPTIONAL, 'Choose table run RDD')
         ->addOption('truncate', 'r', InputOption::VALUE_OPTIONAL, 'Truncate table run RDD')
         ->addOption('detail', 'd', InputOption::VALUE_OPTIONAL, 'Active detail');
	}

	public function __construct()
  {
    parent::__construct();
  }

  protected function execute(InputInterface $input, OutputInterface $output)
	{
  	$this->rddService = $this->getContainer()->get('rdd_service.rdd');
    $this->table = !empty($input->getOption('table')) ?  $input->getOption('table') : $this->table;
    $this->showDetail = !empty($input->getOption('detail')) ?  (bool)$input->getOption('detail') : $this->showDetail;
    $this->truncate = $input->getOption('truncate') == "0" ?  (bool)$input->getOption('truncate') : $this->truncate;
		$this->rddService->generateSQL($this->table, $this->showDetail, $this->truncate);
	}

}
