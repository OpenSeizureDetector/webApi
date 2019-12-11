<?php
// src/Controller/DatapointsController.php

namespace App\Controller;

use Cake\Event\Event;


class DatapointsController extends AppController
{
    // Disable csrf protection for the add event as this does not work for ajax calls.
    // from https://stackoverflow.com/questions/51508171/csrf-token-in-cakephp-when-doing-a-curl-post-request/51959878#51959878
    public function beforeFilter(Event $event)
    {	
        parent::beforeFilter($event);
        //$this->Authentication->allowUnauthenticated(['index']);
        $result = $this->Authentication->getResult();
        if (!$result->isValid()) {
            echo "beforeFilter(): Authentication failed\n";
            print_r($result->getData());
            print_r($result->getErrors());
            $response = $this->response->withStatus(403);
            return $response;            
        }
        else {
            //echo("beforeFilter - Authenticated OK");
        }
    }

    public function index()
    {
        $this->loadComponent('Paginator');
        $user = $this->request->getAttribute('identity');
        $query = $user->applyScope('index', $this->Datapoints->find());
        $datapoints = $this->Paginator->paginate($query);
        
        $this->set(compact('datapoints'));
        $this->set('_serialize', ['datapoints']);
    }

    public function view($id)
    {   
        $datapoint = $this->Datapoints->get($id);
        $this->Authorization->authorize($datapoint);
 

        $this->set(compact('datapoint'));
        $this->set('_serialize', ['datapoint']);
    }

    public function add()
    {
        $this->request->allowMethod(['post', 'put']);
        $datapoint = $this->Datapoints->newEntity();
        $this->Authorization->authorize($datapoint,'create');

        // Interpret the data that has been sent into the correct format.
        $data = $this->request->getData();
        echo("data=".$data);
        $data['dataJSON'] = json_encode($data);
        $data['dataTime'] = $data['dateStr'];

        $accSum = 0.0;
        $nData = 0;
        foreach ($data['rawData'] as $val) {
            $accSum += $val;
            $nData += 1;
        }
        $accMean = $accSum/$nData;
        echo("accMean=".$accMean);
        $data['accMean'] = $accMean;

        $devSq = 0;
        foreach ($data['rawData'] as $val) {
            $devSq += pow($val - $accMean, 2);
        }
        $data['accSd'] = (float)sqrt($devSq/$nData); ;

        $datapoint = $this->Datapoints->patchEntity($datapoint, $data);
        
        if ($this->Datapoints->save($datapoint)) {
            $msg = 'Success';
        } else {
            $msg = 'Failed';
        }
        $this->set([
            'msg' => $msg,
            'datapoint' => $datapoint,
            '_serialize' => ['msg', 'datapoint','data']
        ]);
    }

    public function edit($id) {
        $datapoint = $this->Datapoints->get($id);
        $this->Authorization->authorize($datapoint);
        $this->Datapoints->patchEntity($datapoint, $this->request->getData());
        
        if ($this->Datapoints->save($datapoint)) {
            $msg="Success";
        } else {
            $msg="Failed";
        }
        $this->set([
            'msg' => $msg,
            'datapoint' => $datapoint,
            '_serialize' => ['msg', 'datapoint']
        ]);
        $this->set('_serialize', ['msg']);
    }


    public function setCategory($id,$cat)
    {
	$datapoint = $this->Datapoints->get($id);
    $this->Authorization->authorize($datapoint);
	$datapoint->category_id = $cat;
	if ($this->Datapoints->save($datapoint)) {
	   $msg="Success";
	} else {
	  $msg="Failed";
	}
    	$this->set(compact('msg'));
	$this->set('_serialize', ['msg']);
    }
}