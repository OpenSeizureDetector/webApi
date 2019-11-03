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
            echo "index(): Authentication failed\n";
            print_r($result->getData());
            print_r($result->getErrors());
            $response = $this->response->withStatus(403);
            return $response;            
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
        $datapoint = $this->Datapoints->newEntity($this->request->getData());
        $this->Authorization->authorize($datapoint,'create');
        if ($this->Datapoints->save($datapoint)) {
            $msg = 'Success';
        } else {
            $msg = 'Failed';
        }
        $this->set([
            'msg' => $msg,
            'datapoint' => $datapoint,
            '_serialize' => ['msg', 'datapoint']
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