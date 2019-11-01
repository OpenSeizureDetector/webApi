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
        $this->Authentication->allowUnauthenticated(['index']);
    }

    public function index()
    {
        $result = $this->Authentication->getResult();
        if ($result->isValid()) {
            echo "Authenticated ok";
        }
        else {
            echo "index(): Authentication failed\n";
            print_r($result->getData());
            print_r($result->getErrors());
            $response = $this->response->withStatus(403);
            return $response;            
        }
                
    if ($this->request->is('post') && !$result->isValid()) {
        $this->Flash->error('Invalid username or password');
    }
        $this->loadComponent('Paginator');
        $datapoints = $this->Paginator->paginate($this->Datapoints->find());
        $this->set(compact('datapoints'));
        $this->set('_serialize', ['datapoints']);
    }

    public function view($id)
    {   
	$datapoint = $this->Datapoints->findById($id);
    	$this->set(compact('datapoint'));
	$this->set('_serialize', ['datapoint']);
    }

    public function add()
    {
        $this->request->allowMethod(['post', 'put']);
        $datapoint = $this->Datapoints->newEntity($this->request->getData());
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

    public function setCategory($id,$cat)
    {
	$datapoint = $this->Datapoints->get($id);
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